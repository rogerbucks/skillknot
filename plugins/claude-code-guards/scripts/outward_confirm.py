#!/usr/bin/env python3
"""Asks the person before anything leaves for a Git host: every `git push`, shown with its repo,
target, commits and files, and any `gh` write to a repo you do not own, or any release.

Usage: a PreToolUse hook on Bash (see ../hooks/hooks.json). To try it by hand:
  echo '{"tool_name":"Bash","tool_input":{"command":"git push"},"cwd":"."}' | python3 outward_confirm.py
Writes: nothing. It reads the repo with read-only git commands.

Owners you trust for `gh` writes go in the overlay as "own_github_owners". A push always asks,
because the point is to see what is going out. Best effort: it reads the obvious spellings of a
command, never a program that pushes by itself.
"""

import re
import subprocess
import sys

from guardlib import run, segments

MAX_COMMITS = 10
MAX_FILES = 20
GH_WRITES = {
    "pr": {
        "create",
        "merge",
        "comment",
        "close",
        "reopen",
        "edit",
        "review",
        "ready",
        "lock",
        "unlock",
    },
    "issue": {
        "create",
        "comment",
        "close",
        "reopen",
        "edit",
        "delete",
        "transfer",
        "lock",
        "unlock",
        "pin",
        "unpin",
    },
    "release": {"create", "edit", "delete", "upload", "delete-asset"},
    "repo": {
        "create",
        "fork",
        "edit",
        "delete",
        "archive",
        "unarchive",
        "rename",
        "sync",
        "deploy-key",
    },
    "workflow": {"run", "enable", "disable"},
    "run": {"rerun", "cancel", "delete"},
    "label": {"create", "edit", "delete", "clone"},
    "secret": {"set", "delete"},
    "variable": {"set", "delete"},
}
TAG_REF = re.compile(r"^\+?(?:[^:]*:)?(?:refs/tags/|v?\d+\.\d+\.\d+(?:[-.][\w.]+)?$)")


def git_options(parts, cwd):
    """The folder a git command runs in, and the index of its subcommand."""
    i, folder = 1, cwd
    while i < len(parts) and parts[i].startswith("-"):
        if parts[i] == "-C" and i + 1 < len(parts):
            folder = (
                parts[i + 1]
                if parts[i + 1].startswith("/")
                else f"{folder}/{parts[i + 1]}"
            )
            i += 2
        elif parts[i] == "-c":
            i += 2
        else:
            i += 1
    return folder, i


def pushes_in(command, cwd, home=None):
    """Every git push in a command, as a dict of where it runs and what it sends."""
    found = []
    for parts, here in segments(command, cwd, home):
        if parts[0] != "git":
            continue
        folder, i = git_options(parts, here)
        if i >= len(parts) or parts[i] != "push":
            continue
        args = parts[i + 1 :]
        plain = [a for a in args if not a.startswith("-")]
        remote, refspecs = (plain[0], plain[1:]) if plain else ("origin", [])
        found.append(
            {
                "dir": folder,
                "remote": remote,
                "refspecs": refspecs,
                "force": any(
                    a in ("-f", "--force") or a.startswith("--force-with-lease")
                    for a in args
                )
                or any(r.startswith("+") for r in refspecs),
                "delete": any(a in ("-d", "--delete") for a in args),
                "tags": any(a in ("--tags", "--follow-tags") for a in args)
                or any(TAG_REF.match(r) for r in refspecs),
                "all": any(a in ("--all", "--mirror") for a in args),
            }
        )
    return found


def owner_of(spec):
    """The owner in `owner/name` or a GitHub URL, or None."""
    spec = spec.strip()
    url = re.match(
        r"^(?:https?://|ssh://)?(?:[^@/\s]+@)?github\.com[:/]([^/\s]+)/[^/\s]+?(?:\.git)?/?$",
        spec,
        re.IGNORECASE,
    )
    if url:
        return url.group(1)
    short = re.match(r"^([A-Za-z0-9-]+)/[A-Za-z0-9._-]+$", spec)
    return short.group(1) if short else None


def repo_name(url):
    """'owner/name on host' from a remote URL, with any user or token dropped."""
    url = url.strip().rstrip("/")
    match = re.match(
        r"^(?:[a-z+]+://)?(?:[^@/]+@)?([^/:]+)[:/]([^/]+/[^/]+?)(?:\.git)?$",
        url,
        re.IGNORECASE,
    )
    return (
        f"{match.group(2)} on {match.group(1)}"
        if match and "." in match.group(1)
        else url
    )


def git(folder, *args):
    try:
        done = subprocess.run(
            ["git", "-C", folder, *args],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        return done.returncode == 0, done.stdout
    except (OSError, subprocess.SubprocessError):
        return False, ""


def capped(lines, most):
    return (
        lines[:most] + [f"  and {len(lines) - most} more"]
        if len(lines) > most
        else lines
    )


def summarise(push, reader=git):
    ok, url = reader(push["dir"], "remote", "get-url", push["remote"])
    if not ok:
        return f"Repo: the remote {push['remote']} could not be read"
    lines = [f"Repo: {repo_name(url)}"]
    if push["delete"]:
        return "\n".join(
            lines + [f"Target: DELETES {r} on the remote" for r in push["refspecs"]]
        )
    if push["all"]:
        lines.append("Target: EVERY branch")
    for refspec in [] if push["all"] else push["refspecs"] or [None]:
        spec = (refspec or "").lstrip("+")
        source, _, target = spec.partition(":")
        current = reader(push["dir"], "rev-parse", "--abbrev-ref", "HEAD")[1].strip()
        source = source or current
        target = target or source
        known = reader(
            push["dir"],
            "rev-parse",
            "--verify",
            "-q",
            f"refs/remotes/{push['remote']}/{target}",
        )[0]
        lines.append(
            f"Target: {target}{'' if known else ' (new on the remote)'}"
            f"{' - FORCE, can overwrite history' if push['force'] else ''}"
        )
        ok, log = reader(
            push["dir"],
            "log",
            "--format=%h %s",
            source,
            "--not",
            f"--remotes={push['remote']}",
        )
        commits = [c[:80] for c in log.splitlines() if c]
        if not ok:
            lines.append(f"Commits: could not be read for {source}")
            continue
        lines.append(f"Commits ({len(commits)}):" if commits else "Commits: none new")
        lines += capped([f"  {c}" for c in commits], MAX_COMMITS)
        changed = reader(
            push["dir"],
            "log",
            "--format=",
            "--name-status",
            "--no-renames",
            source,
            "--not",
            f"--remotes={push['remote']}",
        )[1]
        files = {}
        for row in changed.splitlines():
            status, _, name = row.partition("\t")
            if name and name not in files:
                files[name] = status
        if files:
            lines.append(f"Files ({len(files)}):")
            lines += capped([f"  {files[n]} {n}" for n in sorted(files)], MAX_FILES)
    if push["tags"]:
        lines.append("Tags: also pushed, which can cut a release")
    return "\n".join(lines)


def gh_acts(command, cwd, home=None):
    """(what, owner or None, is_release) for each gh command that writes."""
    acts = []
    for parts, here in segments(command, cwd, home):
        if parts[0] != "gh" or len(parts) < 2:
            continue
        repo = None
        for i, word in enumerate(parts):
            if word in ("-R", "--repo") and i + 1 < len(parts):
                repo = parts[i + 1]
            elif word.startswith("--repo="):
                repo = word.split("=", 1)[1]
        if parts[1] == "api":
            method = next(
                (
                    parts[i + 1].upper()
                    for i, w in enumerate(parts[:-1])
                    if w in ("-X", "--method")
                ),
                None,
            )
            fields = any(
                re.match(r"^(-f|-F|--field|--raw-field|--input)(=|$)", w) for w in parts
            )
            if (method == "GET") or (method is None and not fields):
                continue
            endpoint = next((w for w in parts[2:] if re.match(r"^/?repos/", w)), "")
            match = re.match(r"^/?repos/([^/]+)/", endpoint)
            release = "/releases" in endpoint or any("refs/tags" in w for w in parts)
            acts.append(
                (
                    f"gh api {method or 'POST'}",
                    match.group(1) if match else owner_of(repo or ""),
                    release,
                )
            )
        elif len(parts) > 2 and parts[2] in GH_WRITES.get(parts[1], ()):
            named = (
                next((w for w in parts[3:] if not w.startswith("-")), None)
                if parts[1] == "repo"
                else None
            )
            spec = named if named and "/" in named else repo
            owner = owner_of(spec) if spec else None
            if owner is None and not spec:
                ok, url = git(here, "remote", "get-url", "origin")
                owner = owner_of(url) if ok else None
            acts.append((f"gh {parts[1]} {parts[2]}", owner, parts[1] == "release"))
    return acts


def decide(event, config):
    if event.get("tool_name") != "Bash":
        return None
    command = (event.get("tool_input") or {}).get("command", "")
    cwd = event.get("cwd") or "."
    reasons = [summarise(p) for p in pushes_in(command, cwd)]
    own = {o.lower() for o in config.get("own_github_owners", [])}
    for what, owner, release in gh_acts(command, cwd):
        if release or (owner or "").lower() not in own:
            why = (
                "a release"
                if release
                else f"repo owner {owner or 'unknown'} is not in your own list"
            )
            reasons.append(f"{what}: {why}")
    if not reasons:
        return None
    return "ask", "Outward check. This would send:\n\n" + "\n\n".join(
        reasons
    ) + "\n\nApprove only if this is what you meant to publish."


if __name__ == "__main__":
    sys.exit(run("outward", decide))
