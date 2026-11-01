#!/usr/bin/env python3
"""A Claude Code status line: branch, unpushed commits and changed files, context used, session
cost against its cap, time, and whether the SkillKnot guards are installed.

Usage: set as the statusLine command in Claude Code's settings (see the skill). To try it by hand:
  echo '{"session_id":"t","workspace":{"current_dir":"."},"cost":{"total_cost_usd":0.4}}' | python3 statusline.py
Writes: one small JSON file per session in the system temp folder, holding the last cost, time and
context reading, so the session cap can read them. It runs read-only git commands.
"""

import json
import subprocess
import sys
import time
from pathlib import Path

from meterlib import load_config, session_file, write_json

INSTALLED = Path.home() / ".claude" / "plugins" / "installed_plugins.json"
GUARDS_OVERLAY = Path.home() / ".config" / "skillknot" / "claude-code-guards.json"


def git(cwd, *args):
    try:
        done = subprocess.run(
            ["git", "-C", cwd, *args],
            capture_output=True,
            text=True,
            timeout=1,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return done.stdout.strip() if done.returncode == 0 else None


def git_part(cwd):
    branch = git(cwd, "symbolic-ref", "--short", "-q", "HEAD") or git(
        cwd, "rev-parse", "--short", "HEAD"
    )
    if branch is None:
        return None
    part = f"⎇ {branch}"
    ahead = git(cwd, "rev-list", "--count", "@{upstream}..HEAD")
    if ahead is None:
        part += " (not pushed)"
    elif ahead != "0":
        part += f" ↑{ahead}"
    changed = git(cwd, "status", "--porcelain")
    if changed:
        part += f" ●{len(changed.splitlines())}"
    return part


def guards_part():
    """Shows the guards' state only when it can be read. Silence means unknown, never safe."""
    try:
        installed = "claude-code-guards" in INSTALLED.read_text(encoding="utf-8")
    except OSError:
        return None
    if not installed:
        return "guards: not installed"
    try:
        off = json.loads(GUARDS_OVERLAY.read_text(encoding="utf-8")).get("off", [])
    except (OSError, ValueError, AttributeError):
        off = []
    return f"guards off: {', '.join(off)}" if off else "guards on"


def money(value):
    return f"${value:.2f}"


def line(data, config):
    cwd = (data.get("workspace") or {}).get("current_dir") or data.get("cwd") or "."
    cost = data.get("cost") or {}
    usd = cost.get("total_cost_usd")
    minutes = int((cost.get("total_duration_ms") or 0) / 60000)
    context = (data.get("context_window") or {}).get("used_percentage")
    parts = [git_part(cwd)]
    if context is not None:
        parts.append(f"ctx {int(context)}%" + (" ⚠" if context >= 80 else ""))
    if usd is not None:
        cap = config.get("max_usd")
        parts.append(money(usd) + (f" of {money(cap)}" if cap else ""))
    if minutes:
        parts.append(
            f"{minutes // 60}h{minutes % 60:02d}" if minutes >= 60 else f"{minutes}m"
        )
    parts.append(guards_part())
    return " │ ".join(p for p in parts if p)


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        data = {}
    config = load_config()
    print(line(data, config))
    cost = data.get("cost") or {}
    try:
        write_json(
            session_file("reading", data.get("session_id")),
            {
                "usd": cost.get("total_cost_usd"),
                "minutes": (cost.get("total_duration_ms") or 0) / 60000,
                "context": (data.get("context_window") or {}).get("used_percentage"),
                "at": time.time(),
            },
        )
    except OSError:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
