#!/usr/bin/env python3
"""Keeps the agent away from secrets: refuses tool calls that name a secret-shaped path, asks
before credential tools run, and asks before credential-shaped text is written to a file.

Usage: a PreToolUse hook on every tool (see ../hooks/hooks.json). To try it by hand:
  echo '{"tool_name":"Read","tool_input":{"file_path":"/x/.ssh/id_ed25519"}}' | python3 secret_guard.py
Writes: nothing. Findings name the rule, never the secret.

Paths you trust go in the overlay as "allow_paths": absolute entries match exactly, relative ones
with a / as a path suffix. In a shell command a word that starts like a path is read whole; other
words are read as path-shaped runs, so prose and regex text are not read as one path. A guard sees
words, not intent: it
catches the plain spellings and the honest mistakes, and the sandbox remains the real boundary.
"""

import re
import sys

from guardlib import run, segments

# A path part that is itself a secret store, or a file that usually holds one.
STORES = r"(^|/)(\.ssh|\.gnupg|\.aws|\.azure|\.kube|\.docker|\.config/gcloud|\.config/op|\.password-store)(/|$)"
STORE = re.compile(STORES, re.IGNORECASE)
SECRET_PART = re.compile(
    STORES + r"|(^|/)[^/]*secret[^/]*/|(^|/)[^/]*secrets?$"
    r"|(^|/)(\.env(\.[\w.-]+)?|\.netrc|\.npmrc|\.pypirc|credentials(\.json)?|id_(rsa|dsa|ecdsa|ed25519)(\.pub)?)$"
    r"|\.(pem|key|p12|pfx|keychain-db|kdbx)$",
    re.IGNORECASE,
)
# Example files are fine to read: .env.example, .env.sample, .env.template.
EXAMPLE = re.compile(r"\.(example|sample|template|dist)$", re.IGNORECASE)
# Commands that fetch or reveal credentials.
CREDENTIAL_TOOLS = re.compile(r"^(op|bw|lpass|pass|gopass|vault|aws-vault|security)$")
READERS = {
    "cat",
    "less",
    "more",
    "head",
    "tail",
    "cp",
    "mv",
    "scp",
    "rsync",
    "tar",
    "zip",
    "base64",
    "xxd",
    "od",
    "strings",
    "open",
    "source",
    ".",
    "grep",
    "rg",
    "sed",
    "awk",
    "curl",
    "nc",
}
SECURITY_READS = {
    "find-generic-password",
    "find-internet-password",
    "dump-keychain",
    "export",
}
# Text that looks like a live credential.
CREDENTIAL_TEXT = re.compile(
    r"(gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}"
    r"|xox[abpr]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{35}|-----BEGIN [A-Z ]*PRIVATE KEY-----)"
)
PATH_KEYS = (
    "file_path",
    "path",
    "notebook_path",
    "directory",
    "dir",
    "target",
    "source",
    "destination",
)
TEXT_KEYS = ("content", "new_string", "new_source", "text", "body")


# A run of characters that can be part of one path. Whitespace, quotes, backticks, < >, shell
# operators, commas and backslashes end a run, so prose and regex text inside a quoted argument
# are not joined into one long "path". Globs, braces and brackets stay inside a run.
PATH_RUN = re.compile(r"[^\s'\"`<>|;&,\\]+")
# A word that starts like a path is read whole, exactly as before: spaces and all.
ANCHORED = re.compile(r"^(~|\.{1,2}/|/|\$HOME\b|\$\{HOME\})")
# Characters that continue a file or folder name, used to keep allow entries to whole names.
NAME_CHAR = r"[\w.\-]"


def strip_dot(path):
    return re.sub(r"^(\./)+", "", path)


def suffix_entries(allowed):
    """Relative allow entries that may match as a path suffix: they contain a /, and neither name
    a secret file (.env, id_rsa, *.pem ...) as their last part nor sit inside a secret store such
    as .ssh. Any other entry matches only exactly."""
    found = []
    for entry in allowed:
        entry = strip_dot(str(entry)).rstrip("/")
        if (
            "/" in entry
            and not entry.startswith(("/", "~"))
            and not SECRET_PART.search(entry.rsplit("/", 1)[-1])
            and not STORE.search(entry)
        ):
            found.append(
                re.compile(rf"(?<!{NAME_CHAR}){re.escape(entry)}(?!{NAME_CHAR}|/)")
            )
    return found


def unallowed(path, allowed=()):
    """The path left to check once allow_paths is applied, or None when it is allowed outright.
    An entry matches the whole path exactly (a leading ./ aside). A suffix entry also matches
    wherever it ends a path, so one entry covers every checkout and worktree; it is replaced by
    a / and the text before it is still checked, so it never excuses a secret folder above it.
    An entry covers that one path, never what is under it."""
    if path in allowed or strip_dot(path) in {strip_dot(str(a)) for a in allowed}:
        return None
    for entry in suffix_entries(allowed):
        path = entry.sub("/", path)
    return path


def secret_path(path, allowed=()):
    """True when a path looks like a secret store and allow_paths does not cover it."""
    if not path or EXAMPLE.search(path):
        return False
    rest = unallowed(path, allowed)
    return rest is not None and bool(SECRET_PART.search(rest))


def secret_word(word, allowed=()):
    """True when one shell word names a secret-shaped path. Pieces cut at = : , are read whole
    when they start like a path. Other pieces are read as path-shaped runs, and in a piece with
    whitespace (prose, a message) only runs with a / count, so a sentence that mentions a file
    is not one long path. An example-file name is exempt only where it ends the run's text."""
    for token in re.split(r"[=:,]", word):
        if not token or token in allowed:
            continue
        if ANCHORED.match(token):
            if secret_path(token, allowed):
                return True
            continue
        prose = bool(re.search(r"\s", token))
        for match in PATH_RUN.finditer(token):
            run = match.group()
            if prose and "/" not in run:
                continue
            after = token[match.end() : match.end() + 1]
            if EXAMPLE.search(run) and (not after or after in " \t\n'\"`"):
                continue
            rest = unallowed(run, allowed)
            if rest is not None and SECRET_PART.search(rest):
                return True
    return False


def paths_in(tool_input):
    found = [
        str(tool_input[k]) for k in PATH_KEYS if isinstance(tool_input.get(k), str)
    ]
    for value in tool_input.values():
        if isinstance(value, list):
            found += [v for v in value if isinstance(v, str) and "/" in v]
    return found


def command_findings(command, cwd, allowed=()):
    """(decision, rule) pairs for one shell command."""
    findings = []
    for parts, _ in segments(command, cwd):
        tool = parts[0].rsplit("/", 1)[-1]
        if CREDENTIAL_TOOLS.match(tool) and (
            tool != "security" or (len(parts) > 1 and parts[1] in SECURITY_READS)
        ):
            findings.append(("ask", f"runs `{tool}`, which can reveal credentials"))
        for word in parts[1:]:
            if secret_word(word, allowed):
                findings.append(
                    (
                        "deny" if tool in READERS else "ask",
                        "names a secret-shaped path",
                    )
                )
    return findings


def decide(event, config):
    tool = event.get("tool_name", "")
    data = event.get("tool_input") or {}
    allowed = tuple(config.get("allow_paths", []))
    findings = []
    if tool == "Bash":
        findings += command_findings(
            data.get("command", ""), event.get("cwd") or ".", allowed
        )
    else:
        if any(secret_path(p, allowed) for p in paths_in(data)):
            findings.append(("deny", "names a secret-shaped path"))
        pattern = data.get("pattern") or data.get("glob") or ""
        if isinstance(pattern, str) and re.search(
            r"secret|\.env\b|\.ssh|\.pem|id_rsa", pattern, re.IGNORECASE
        ):
            findings.append(("ask", "searches for secret-shaped files"))
        if any(
            isinstance(data.get(k), str) and CREDENTIAL_TEXT.search(data[k])
            for k in TEXT_KEYS
        ):
            findings.append(("ask", "writes text that looks like a live credential"))
    if not findings:
        return None
    decision = "deny" if any(d == "deny" for d, _ in findings) else "ask"
    rules = "; ".join(sorted({rule for _, rule in findings}))
    tail = (
        " If it is safe, add the exact path, or a relative path that ends it, to allow_paths in"
        " ~/.config/skillknot/claude-code-guards.json."
        if decision == "deny"
        else ""
    )
    return (
        decision,
        f"Secret guard: this call {rules}.{tail} Do not reword or re-encode the call to get past this.",
    )


if __name__ == "__main__":
    sys.exit(run("secret", decide))
