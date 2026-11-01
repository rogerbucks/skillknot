"""Shared helpers for the claude-code-guards hooks: read the hook input, split shell commands,
load the personal overlay, and answer Claude Code.

Usage: imported by the hook scripts beside it.
Writes: nothing.

The overlay is optional JSON at ~/.config/skillknot/claude-code-guards.json, for example:
  {"own_github_owners": ["your-handle"], "allow_paths": ["/exact/path/you/trust"], "off": ["connector"]}
"""

import json
import os
import re
import shlex
import sys
from pathlib import Path

OVERLAY = Path.home() / ".config" / "skillknot" / "claude-code-guards.json"
SEPARATORS = re.compile(r"&&|\|\||[;|\n]")


def load_config(path=None):
    """The overlay as a dict, or {} when it is missing or unreadable."""
    target = (
        Path(path) if path else Path(os.environ.get("SKILLKNOT_GUARDS_CONFIG", OVERLAY))
    )
    try:
        return json.loads(target.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def is_off(config, guard):
    return guard in config.get("off", [])


def words(segment):
    """Shell words of one command segment, without redirections. Falls back to a plain split."""
    try:
        parts = shlex.split(segment, comments=False)
    except ValueError:
        parts = segment.split()
    return [w for w in parts if not re.match(r"^\d*[<>]", w)]


def expand(path, cwd, home=None):
    home = home or str(Path.home())
    path = re.sub(r"^(~|\$HOME|\$\{HOME\})(?=/|$)", home, path)
    return path if path.startswith("/") else os.path.normpath(os.path.join(cwd, path))


def segments(command, cwd, home=None):
    """Yields (words, cwd) for each simple command, following `cd` so later segments know their folder.
    Leading VAR=value assignments are dropped. Best effort: it reads the obvious spellings only."""
    here = cwd
    for segment in SEPARATORS.split(command or ""):
        parts = words(segment)
        while parts and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", parts[0]):
            parts = parts[1:]
        if not parts:
            continue
        if parts[0] == "cd" and len(parts) > 1:
            here = expand(parts[1], here, home)
            continue
        yield parts, here


def read_input():
    try:
        return json.load(sys.stdin)
    except ValueError:
        return {}


def answer(decision, reason):
    """Prints a PreToolUse decision: "ask", "deny" or "allow"."""
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": decision,
                    "permissionDecisionReason": reason,
                }
            }
        )
    )


def run(guard_name, decide):
    """Runs one guard. `decide(event, config)` returns None to stay silent, or (decision, reason).
    A guard that fails asks the person rather than letting the call through unseen."""
    event = read_input()
    config = load_config()
    if is_off(config, guard_name):
        return 0
    try:
        result = decide(event, config)
    except Exception as error:  # noqa: BLE001 - a broken guard must not wave a call through
        result = (
            "ask",
            f"{guard_name}: the guard failed ({type(error).__name__}), so a person should check this call.",
        )
    if result:
        answer(*result)
    return 0
