#!/usr/bin/env python3
"""Looks for a person's private words in a Git repo, and never shows a word.

Usage: python3 scan.py [--list PATH] [--repo PATH] [--history] [--allow WORD] [--set-secret NAME] [--where]
Writes: nothing, unless --set-secret stores the words as a GitHub Actions secret

The list is found in this order: --list, then SKILLKNOT_TERMS_FILE, then
~/.config/skillknot/blocked-terms.md. A Markdown list takes only its bullets, so it can hold notes.
Any other file takes one word a line. A list inside a Git repo is refused.

File names are masked with *** wherever they hold a word. History covers commit authors, their
emails, messages and every line a commit added.

Exit 0 means nothing was found, 1 means something was, and 2 means the scan could not run.
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


def list_path(named):
    if named:
        return Path(named)
    if os.environ.get("SKILLKNOT_TERMS_FILE"):
        return Path(os.environ["SKILLKNOT_TERMS_FILE"])
    return Path.home() / ".config" / "skillknot" / "blocked-terms.md"


def parse_words(name, text):
    if str(name).endswith(".md"):
        body = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.DOTALL)
        bullets = (
            line[2:].strip()
            for line in body.splitlines()
            if line.startswith(("- ", "* "))
        )
        return [bullet for bullet in bullets if bullet]
    lines = (line.strip() for line in text.splitlines())
    return [line for line in lines if line and not line.startswith("#")]


def in_git_repo(path):
    found = subprocess.run(
        ["git", "-C", str(path.resolve().parent), "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True,
        check=False,
    )
    return found.stdout.strip() == "true"


def has_word(text, words, allow):
    lowered = text.lower()
    for word in allow:
        lowered = lowered.replace(word.lower(), "")
    return any(word.lower() in lowered for word in words)


def mask(name, words):
    for word in sorted(words, key=len, reverse=True):
        name = re.sub(re.escape(word), "***", name, flags=re.IGNORECASE)
    return name


def repo_files(repo):
    listing = subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return listing.stdout.splitlines()


def scan_files(repo, words, allow):
    found = []
    for name in repo_files(repo):
        shown = mask(name, words)
        if has_word(name, words, allow):
            found.append(f"{shown}: in the file name")
        try:
            text = (repo / name).read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError):
            continue
        found += [
            f"{shown}:{number}"
            for number, line in enumerate(text.splitlines(), 1)
            if has_word(line, words, allow)
        ]
    return found


def scan_history(repo, words, allow):
    log = subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "log",
            "--all",
            "-p",
            "--no-color",
            "--format=%x01%h%x00%an%x00%ae%x00%B%x02",
        ],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )
    found = []
    for record in log.stdout.split("\x01")[1:]:
        commit, _, rest = record.partition("\x00")
        details, _, changes = rest.partition("\x02")
        if has_word(details, words, allow):
            found.append(f"commit {commit}: in its author or message")
        if any(
            line.startswith("+") and has_word(line, words, allow)
            for line in changes.splitlines()
        ):
            found.append(f"commit {commit}: in a file it changed")
    return found


def run(args):
    path = list_path(args.list)
    if args.where:
        print(path)
    if not path.is_file():
        print("The private list was not found. Name it with --list.", file=sys.stderr)
        return 2
    if in_git_repo(path):
        print(
            "The private list is inside a Git repo. Move it out first.", file=sys.stderr
        )
        return 2
    words = parse_words(path, path.read_text(encoding="utf-8"))
    if not words:
        print("The private list holds no words.", file=sys.stderr)
        return 2
    if args.where:
        print(f"{len(words)} word(s).")
        return 0

    repo = Path(args.repo).resolve()
    if args.set_secret:
        # The words go by standard input, so they reach no command line and no output.
        subprocess.run(
            ["gh", "secret", "set", args.set_secret],
            input="\n".join(words) + "\n",
            text=True,
            cwd=repo,
            check=True,
        )
        print(f"Stored {len(words)} word(s) as {args.set_secret}.")
        return 0

    found = scan_files(repo, words, args.allow)
    if args.history:
        found += scan_history(repo, words, args.allow)
    for place in found:
        print(place)
    print(f"{len(found)} place(s) found; {len(words)} word(s) checked.")
    return 1 if found else 0


def main():
    parser = argparse.ArgumentParser(
        description="Look for private words in a Git repo."
    )
    parser.add_argument("--list", help="the private list, outside any Git repo")
    parser.add_argument("--repo", default=".", help="the repo to scan")
    parser.add_argument(
        "--history", action="store_true", help="also read commit authors and messages"
    )
    parser.add_argument(
        "--allow",
        action="append",
        default=[],
        help="a longer word that is fine, such as a handle",
    )
    parser.add_argument(
        "--set-secret",
        metavar="NAME",
        help="store the words as this GitHub Actions secret",
    )
    parser.add_argument(
        "--where",
        action="store_true",
        help="show the list's path and word count, and stop",
    )
    args = parser.parse_args()
    try:
        return run(args)
    except (OSError, UnicodeError, subprocess.CalledProcessError) as error:
        print(f"The scan could not run: {type(error).__name__}.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
