#!/usr/bin/env python3
"""Asks the person before a shell command that destroys work and cannot be undone: recursive
deletes, discarding Git changes, dropping database tables, wiping disks and tearing down
infrastructure.

Usage: a PreToolUse hook on Bash (see ../hooks/hooks.json). To try it by hand:
  echo '{"tool_name":"Bash","tool_input":{"command":"git reset --hard"},"cwd":"."}' | python3 destructive_guard.py
Writes: nothing.

Folders you rebuild often, such as node_modules, go in the overlay as "rebuildable": a recursive
delete of only those names then runs without a prompt. Best effort: it reads the obvious spellings
of a command. A script that deletes by itself is not seen, and the sandbox covers that.
"""

import re
import sys

from guardlib import run, segments

SQL = re.compile(
    r"\b(drop\s+(table|database|schema|index|view)|truncate\s+(table\s+)?\w)",
    re.IGNORECASE,
)
DELETE_NO_WHERE = re.compile(
    r"\bdelete\s+from\s+[\w.\"`]+\s*(;|$|[\"'])", re.IGNORECASE
)
WHOLE_TREE = {".", "./", "*", "./*", ":/"}


def flags(parts):
    """Short and long options of one command, with short clusters split into single letters."""
    found = set()
    for word in parts[1:]:
        if word == "--":
            break
        if word.startswith("--"):
            found.add(word.split("=", 1)[0])
        elif word.startswith("-") and len(word) > 1:
            found.update(f"-{letter}" for letter in word[1:])
    return found


def operands(parts):
    return [w for w in parts[1:] if not w.startswith("-")]


def git_verb(parts):
    """The Git subcommand and its own words, skipping options such as -C <dir> before it."""
    rest = parts[1:]
    while rest and rest[0].startswith("-"):
        rest = rest[2:] if rest[0] in ("-C", "-c") else rest[1:]
    return (rest[0], ["git", *rest[1:]]) if rest else ("", [])


def rm_risk(parts, rebuildable):
    found = flags(parts)
    if not found & {"-r", "-R", "--recursive"}:
        return None
    targets = operands(parts)
    names = {t.rstrip("/").rsplit("/", 1)[-1] for t in targets}
    if targets and names <= set(rebuildable):
        return None
    return f"`rm` deletes folders and everything in them: {' '.join(targets) or '(no path)'}"


def git_risk(parts):
    verb, sub = git_verb(parts)
    found = flags(sub)
    paths = operands(sub)
    if verb == "reset" and "--hard" in found:
        return "`git reset --hard` throws away every uncommitted change"
    if verb == "clean" and found & {"-f", "--force"}:
        return "`git clean -f` deletes untracked files, which Git cannot bring back"
    whole_tree = set(paths) & WHOLE_TREE or (
        verb == "checkout" and "--" in sub and not paths
    )
    if verb in ("checkout", "restore") and "--staged" not in found and whole_tree:
        return f"`git {verb} .` throws away uncommitted changes to every file"
    if verb == "branch" and ("-D" in found or {"-d", "--force"} <= found):
        return "`git branch -D` deletes a branch even if its work was never merged"
    if verb == "stash" and paths[:1] in (["drop"], ["clear"]):
        return f"`git stash {paths[0]}` deletes saved work"
    return None


def other_risk(parts):
    program = parts[0].rsplit("/", 1)[-1]
    words = parts[1:]
    if program == "find" and (
        "-delete" in words or ("-exec" in words and "rm" in words)
    ):
        return "`find` deletes every file it matches"
    if program == "dd" and any(w.startswith("of=/dev/") for w in words):
        return "`dd` writes straight onto a disk"
    if program.startswith("mkfs") or program in ("shred", "wipefs"):
        return f"`{program}` wipes a disk or file for good"
    if program == "terraform" and words[:1] == ["destroy"]:
        return "`terraform destroy` tears down real infrastructure"
    if program == "kubectl" and words[:1] == ["delete"]:
        return "`kubectl delete` removes live cluster resources"
    if program == "docker" and words[:2] in (["system", "prune"], ["volume", "prune"]):
        return f"`docker {' '.join(words[:2])}` deletes stored data"
    recursive = flags(parts) & {"-R", "--recursive"}
    if (
        program in ("chmod", "chown")
        and recursive
        and any(t in ("/", "~", "/*") for t in operands(parts))
    ):
        return f"`{program} -R` on a whole system or home folder"
    return None


def risks(command, cwd, rebuildable=()):
    found = []
    for parts, _here in segments(command, cwd):
        program = parts[0].rsplit("/", 1)[-1]
        if program == "sudo" and len(parts) > 1:
            parts = parts[1:]
            program = parts[0].rsplit("/", 1)[-1]
        if program == "rm":
            reason = rm_risk(parts, rebuildable)
        elif program == "git":
            reason = git_risk(parts)
        else:
            reason = other_risk(parts)
        if reason:
            found.append(reason)
    if SQL.search(command or ""):
        found.append("a SQL `DROP` or `TRUNCATE` removes a table and its data")
    if DELETE_NO_WHERE.search(command or ""):
        found.append("a SQL `DELETE` with no `WHERE` empties the whole table")
    return found


def decide(event, config):
    if event.get("tool_name") != "Bash":
        return None
    command = (event.get("tool_input") or {}).get("command", "")
    found = risks(command, event.get("cwd") or ".", config.get("rebuildable", []))
    if not found:
        return None
    lines = "\n".join(f"- {reason}" for reason in found)
    return (
        "ask",
        f"Destructive command. This cannot be undone:\n{lines}\nApprove it only if losing this is intended.",
    )


if __name__ == "__main__":
    sys.exit(run("destructive", decide))
