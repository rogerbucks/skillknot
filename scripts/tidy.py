#!/usr/bin/env python3
"""Puts every text file in one layout, so nothing varies for a tool or an agent to misread.

Usage: python3 scripts/tidy.py [--check] [--staged]
Writes: tracked text files, in place (with --check, nothing)

--check lists what would change and exits 1, which is how CI uses it. --staged tidies only the
files about to be committed and stages the result, which is how the pre-commit hook uses it.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

SKILL_CHARACTERS = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"', " ": " "})


def tidy_text(name, text):
    lines = [
        line.rstrip()
        for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    ]
    tidied = "\n".join(lines).rstrip("\n")
    if name.startswith("plugins/") and name.endswith(".md"):
        tidied = tidied.translate(SKILL_CHARACTERS)
    if name.endswith(".json"):
        try:
            tidied = json.dumps(json.loads(tidied), indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            pass  # check.py reports it
    return f"{tidied}\n" if tidied else ""


def tidy_files(root, files, fix):
    changed = []
    for name in files:
        path = root / name
        try:
            with path.open(encoding="utf-8", newline="") as file:
                text = file.read()
        except (UnicodeDecodeError, FileNotFoundError):
            continue
        tidied = tidy_text(name, text)
        if tidied != text:
            changed.append(name)
            if fix:
                with path.open("w", encoding="utf-8", newline="") as file:
                    file.write(tidied)
    return changed


def listed(root, *args):
    return subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True, check=True
    ).stdout.splitlines()


def main():
    parser = argparse.ArgumentParser(description="Put every text file in one layout.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="list what would change, and exit 1 if anything would",
    )
    parser.add_argument(
        "--staged", action="store_true", help="tidy and restage only the staged files"
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    files = (
        listed(root, "diff", "--cached", "--name-only", "--diff-filter=ACM")
        if args.staged
        else listed(root, "ls-files")
    )
    changed = tidy_files(root, files, fix=not args.check)
    for name in changed:
        print(f"{'would tidy' if args.check else 'tidied'} {name}")
    if args.staged and changed:
        subprocess.run(["git", "-C", str(root), "add", "--", *changed], check=True)
    return 1 if args.check and changed else 0


if __name__ == "__main__":
    sys.exit(main())
