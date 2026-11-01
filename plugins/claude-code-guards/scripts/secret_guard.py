#!/usr/bin/env python3
"""Keeps the agent away from secrets: refuses tool calls that name a secret-shaped path, asks
before credential tools run, and asks before credential-shaped text is written to a file.

Usage: a PreToolUse hook on every tool (see ../hooks/hooks.json). To try it by hand:
  echo '{"tool_name":"Read","tool_input":{"file_path":"/x/.ssh/id_ed25519"}}' | python3 secret_guard.py
Writes: nothing. Findings name the rule, never the secret.

Exact paths you trust go in the overlay as "allow_paths". A guard sees words, not intent: it
catches the plain spellings and the honest mistakes, and the sandbox remains the real boundary.
"""

import re
import sys

from guardlib import run, segments

# A path part that is itself a secret store, or a file that usually holds one.
SECRET_PART = re.compile(
    r"(^|/)(\.ssh|\.gnupg|\.aws|\.azure|\.kube|\.docker|\.config/gcloud|\.config/op|\.password-store)(/|$)"
    r"|(^|/)[^/]*secret[^/]*/|(^|/)[^/]*secrets?$"
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


def secret_path(path, allowed=()):
    """True when a path looks like a secret store and is not on the exact allow-list."""
    if not path or path in allowed or EXAMPLE.search(path):
        return False
    return bool(SECRET_PART.search(path))


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
            for token in re.split(r"[=:,]", word):
                if secret_path(token, allowed):
                    findings.append(
                        (
                            "deny" if tool in READERS else "ask",
                            "names a secret-shaped path",
                        )
                    )
                    break
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
        " Add the exact path to allow_paths in ~/.config/skillknot/claude-code-guards.json if it is safe."
        if decision == "deny"
        else ""
    )
    return (
        decision,
        f"Secret guard: this call {rules}.{tail} Do not reword or re-encode the call to get past this.",
    )


if __name__ == "__main__":
    sys.exit(run("secret", decide))
