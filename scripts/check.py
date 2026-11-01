#!/usr/bin/env python3
"""Checks this repo before anything reaches main: no personal details, no hidden text, every skill
well formed, and anything that lets a plugin act named in reviewed-powers.json.

Usage: python3 scripts/check.py [--history] [--require-terms] [--terms-file PATH]
Writes: nothing (read-only)

The private word list is never kept here, because the list would itself be a leak. It comes from
the LEAK_TERMS environment variable, one word a line, or from the bullets of the Markdown note at
~/.config/skillknot/blocked-terms.md. Findings name the file and line and never print the word, because CI logs are public.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ALLOWED_WORDS = ("rogerbucks",)  # the public GitHub handle, which the repo URL shows anyway
DEFAULT_TERMS_FILE = Path.home() / ".config" / "skillknot" / "blocked-terms.md"
MAX_SKILL_LINES = 500
MAX_DESCRIPTION = 1024
MAX_COMPATIBILITY = 500
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MODEL_NAME = re.compile(r"\b(haiku|sonnet|opus|gemini|gpt-?\d[\w.-]*)\b", re.IGNORECASE)
POWER_FOLDERS = ("hooks", "scripts", "agents", "commands", "bin", ".mcp.json", ".lsp.json")
LINK = re.compile(r"\]\((?!https?://|#|mailto:)([^)#\s]+)")

HOME_PATH = re.compile(r"(/(?:Users|home)/[A-Za-z]|[A-Za-z]:\\Users\\)")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9.-]+")
PUBLIC_EMAIL = re.compile(r"(@users\.noreply\.github\.com|^noreply@anthropic\.com|@example\.(com|org))$")
HISTORY_EMAIL = re.compile(r"(@users\.noreply\.github\.com|^noreply@github\.com)$")
SECRET = re.compile(
    r"(gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|sk-[a-z]{2,4}-[A-Za-z0-9_-]{20,}"
    r"|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)"
)


def parse_terms(text):
    lines = (line.strip() for line in text.splitlines())
    return [line for line in lines if line and not line.startswith("#")]


def parse_markdown_terms(text):
    body = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.DOTALL)
    return [line[2:].strip() for line in body.splitlines() if line.startswith("- ") and line[2:].strip()]


def load_terms(terms_file=None):
    terms = parse_terms(os.environ.get("LEAK_TERMS", ""))
    path = Path(terms_file) if terms_file else DEFAULT_TERMS_FILE
    if path.is_file():
        text = path.read_text(encoding="utf-8")
        terms += parse_markdown_terms(text) if path.suffix == ".md" else parse_terms(text)
    return terms


def has_term(text, terms):
    lowered = text.lower()
    for word in ALLOWED_WORDS:
        lowered = lowered.replace(word, "")
    return any(term.lower() in lowered for term in terms)


def check_leaks(root, files, terms):
    findings = []
    for name in files:
        if has_term(name, terms):
            findings.append(f"{name}: the file name holds a blocked word")
        try:
            text = (root / name).read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError):
            continue
        for number, line in enumerate(text.splitlines(), 1):
            where = f"{name}:{number}"
            if HOME_PATH.search(line):
                findings.append(f"{where}: a home folder path")
            if SECRET.search(line):
                findings.append(f"{where}: something shaped like a secret")
            if any(not PUBLIC_EMAIL.search(found) for found in EMAIL.findall(line)):
                findings.append(f"{where}: a personal email address")
            if has_term(line, terms):
                findings.append(f"{where}: a blocked word")
    return findings


def check_hidden(root, files):
    """Finds text a reader would not see, which could carry instructions past a review."""
    findings = []
    for name in files:
        try:
            text = (root / name).read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError):
            continue
        for number, line in enumerate(text.splitlines(), 1):
            if any(unicodedata.category(character) == "Cf" for character in line):
                findings.append(f"{name}:{number}: an invisible character")
        if name.startswith("plugins/") and name.endswith(".md") and "<!--" in text:
            findings.append(f"{name}: an HTML comment, which a reader of the page would not see")
    return findings


def check_powers(root):
    """Names each thing that lets a plugin act, unless reviewed-powers.json records its review."""
    reviewed_file = root / "reviewed-powers.json"
    reviewed = json.loads(reviewed_file.read_text(encoding="utf-8")) if reviewed_file.is_file() else {}
    powers = []
    for plugin in sorted((root / "plugins").glob("*")) if (root / "plugins").is_dir() else []:
        powers += [plugin / power for power in POWER_FOLDERS if (plugin / power).exists()]
        for skill in sorted((plugin / "skills").glob("*/SKILL.md")):
            powers += [skill.parent / power for power in POWER_FOLDERS if (skill.parent / power).exists()]
            fields = frontmatter(skill.read_text(encoding="utf-8")) or {}
            if "allowed-tools" in fields or "hooks" in fields:
                powers.append(skill)
    names = [path.relative_to(root).as_posix() for path in powers]
    return [f"{name}: can act, and is not in reviewed-powers.json" for name in names if name not in reviewed]


def frontmatter(text):
    match = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return None
    fields = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if separator and not key.startswith((" ", "\t")):
            fields[key.strip()] = value.strip()
    return fields


def check_skill(path):
    where = str(path)
    text = path.read_text(encoding="utf-8")
    fields = frontmatter(text)
    if fields is None:
        return [f"{where}: no frontmatter"]
    findings = []
    name = fields.get("name", "")
    if not (NAME.match(name) and len(name) <= 64):
        findings.append(f"{where}: bad name")
    if name != path.parent.name:
        findings.append(f"{where}: name differs from its folder")
    description = fields.get("description", "")
    if not 1 <= len(description) <= MAX_DESCRIPTION:
        findings.append(f"{where}: description missing or over {MAX_DESCRIPTION} characters")
    if not 1 <= len(fields.get("compatibility", "")) <= MAX_COMPATIBILITY:
        findings.append(f"{where}: compatibility missing or over {MAX_COMPATIBILITY} characters")
    if MODEL_NAME.search(text):
        findings.append(f"{where}: a vendor's model name, which belongs in references/models.md")
    if len(text.splitlines()) >= MAX_SKILL_LINES:
        findings.append(f"{where}: {MAX_SKILL_LINES} lines or more")
    for target in LINK.findall(text):
        if not (path.parent / target).exists():
            findings.append(f"{where}: broken link to {target}")
    return findings


def check_format(root):
    entries = json.loads((root / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))["plugins"]
    listed = {entry["name"]: entry["source"] for entry in entries}
    findings = []
    for name, source in listed.items():
        if source != f"./plugins/{name}":
            findings.append(f"marketplace: {name} has an unexpected source")
    readme = root / "README.md"
    readme_text = readme.read_text(encoding="utf-8") if readme.is_file() else ""
    for plugin in sorted((root / "plugins").glob("*")) if (root / "plugins").is_dir() else []:
        if not plugin.is_dir():
            continue
        if plugin.name not in listed:
            findings.append(f"marketplace: {plugin.name} is not listed")
        manifest = plugin / ".claude-plugin" / "plugin.json"
        if not manifest.is_file() or json.loads(manifest.read_text(encoding="utf-8")).get("name") != plugin.name:
            findings.append(f"{plugin.name}: plugin.json name differs from its folder")
        skills = sorted((plugin / "skills").glob("*/SKILL.md"))
        if not skills:
            findings.append(f"{plugin.name}: no skill")
        for skill in skills:
            findings += check_skill(skill)
            if f"`{skill.parent.name}`" not in readme_text:
                findings.append(f"README: {skill.parent.name} is not listed")
    return findings


def check_history(root, terms=()):
    log = subprocess.run(
        ["git", "-C", str(root), "log", "--all", "--format=%h%x00%ae%x00%ce%x00%an%x00%cn%x00%B%x01"],
        capture_output=True, text=True, check=False,
    )
    findings = []
    for record in log.stdout.split("\x01"):
        parts = record.strip().split("\x00")
        if len(parts) < 6:
            continue
        commit, author, committer, *rest = parts
        if not (HISTORY_EMAIL.search(author) and HISTORY_EMAIL.search(committer)):
            findings.append(f"commit {commit}: a personal email address")
        if has_term(" ".join(rest), terms):
            findings.append(f"commit {commit}: a blocked word in its names or message")
    return findings


def tracked_files(root):
    listing = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--cached", "--others", "--exclude-standard"],
        capture_output=True, text=True, check=True,
    )
    return listing.stdout.splitlines()


def main():
    parser = argparse.ArgumentParser(description="Check this repo for leaks and malformed skills.")
    parser.add_argument("--history", action="store_true", help="check commit emails and messages too")
    parser.add_argument("--require-terms", action="store_true", help="fail if no private word list was found")
    parser.add_argument("--terms-file", help="a private word list, one word a line")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    terms = load_terms(args.terms_file)
    if args.require_terms and not terms:
        print("No private word list found.", file=sys.stderr)
        return 1
    files = tracked_files(root)
    findings = check_leaks(root, files, terms) + check_hidden(root, files) + check_format(root) + check_powers(root)
    if args.history:
        findings += check_history(root, terms)
    for finding in findings:
        print(finding, file=sys.stderr)
    print(f"{len(findings)} problem(s); {len(terms)} private word(s) checked.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
