#!/usr/bin/env python3
"""Checks the web links in the repo's Markdown, from your own machine, when you choose to.

Usage: python3 scripts/links.py [PATH ...] [--timeout SECONDS]
Writes: nothing. Prints a report and exits 1 only if a link looks broken

Not part of CI. Many government and legal sites refuse automated checkers (bot challenges, 202
holding pages, HTTP/2 resets, 403s), so a CI job raised mostly false alarms. This script sorts each
link into one of three groups:

- ok: the page answered
- unverified: the site refused, stalled or sent a 202 holding page. That says nothing
  about the link
- broken: a 404 or 410, or the host does not exist. Open it in a browser, or ask an agent to
  fetch it, before changing anything. Some sites send a 404 to checkers too
"""

import argparse
import concurrent.futures
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

LINK = re.compile(r"https?://[^\s<>\"')\]`]+")
BROKEN_STATUS = {404, 410}
AGENT = "Mozilla/5.0 (compatible; skillknot-links/1.0)"


def links_in(text):
    return [url.rstrip(".,;:") for url in LINK.findall(text)]


def classify(status=None, error=None):
    if error == "no such host" or status in BROKEN_STATUS:
        return "broken"
    if status is not None and 200 <= status < 300 and status != 202:
        return "ok"
    return "unverified"


def fetch(url, timeout):
    request = urllib.request.Request(url, headers={"User-Agent": AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return classify(status=response.status), str(response.status)
    except urllib.error.HTTPError as problem:
        return classify(status=problem.code), str(problem.code)
    except urllib.error.URLError as problem:
        reason = str(problem.reason)
        if "Name or service not known" in reason or "nodename nor servname" in reason:
            return classify(error="no such host"), "no such host"
        return classify(error=reason), reason
    except (TimeoutError, OSError) as problem:
        return classify(error=str(problem)), type(problem).__name__


def markdown_files(paths):
    if paths:
        return [Path(path) for path in paths]
    listed = subprocess.run(
        ["git", "ls-files", "*.md"], capture_output=True, text=True, check=True
    ).stdout
    return [Path(name) for name in listed.splitlines()]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "paths", nargs="*", help="Markdown files (default: every tracked one)"
    )
    parser.add_argument("--timeout", type=float, default=15)
    args = parser.parse_args()

    where = {}
    for path in markdown_files(args.paths):
        for url in links_in(path.read_text(encoding="utf-8")):
            where.setdefault(url, []).append(str(path))

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = dict(
            zip(where, pool.map(lambda url: fetch(url, args.timeout), where))
        )

    groups = {"ok": [], "unverified": [], "broken": []}
    for url, (group, detail) in results.items():
        groups[group].append((url, detail))

    for group in ("broken", "unverified"):
        for url, detail in sorted(groups[group]):
            print(f"{group}: {url} ({detail}) in {', '.join(sorted(set(where[url])))}")
    print(
        f"{len(groups['ok'])} ok, {len(groups['unverified'])} unverified, "
        f"{len(groups['broken'])} broken"
    )
    return 1 if groups["broken"] else 0


if __name__ == "__main__":
    sys.exit(main())
