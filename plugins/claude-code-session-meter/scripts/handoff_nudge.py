#!/usr/bin/env python3
"""Reminds the person to run a handoff when a session has changed files for a while and nothing
has been handed off since: the moment where decisions and next steps are most often lost.

Usage: a Stop hook (see ../hooks/hooks.json). To try it by hand:
  echo '{"session_id":"t","transcript_path":"/path/to/transcript.jsonl"}' | python3 handoff_nudge.py
Writes: one small JSON file per session in the system temp folder, recording when it last reminded.

It never stops the agent. It shows one line to the person, at most once per stretch of work, and
again only after a further stretch of edits. A handoff run since the last edit keeps it quiet.
"""

import json
import sys
import time
from pathlib import Path

from meterlib import load_config, read_json, session_file, write_json

EDIT_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}


def tool_uses(transcript_path):
    """Yields (tool name, input) for each tool call in a Claude Code transcript, oldest first."""
    try:
        lines = Path(transcript_path).read_text(encoding="utf-8").splitlines()
    except (OSError, TypeError):
        return
    for raw in lines:
        try:
            entry = json.loads(raw)
        except ValueError:
            continue
        content = (entry.get("message") or {}).get("content")
        if not isinstance(content, list):
            continue
        for block in content:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                yield block.get("name", ""), block.get("input") or {}


def is_handoff(name, tool_input):
    text = json.dumps(tool_input).lower()
    return name in ("Skill", "SlashCommand") and "handoff" in text


def edit_counts(transcript_path):
    """(edits since the last handoff, edits in the whole session)."""
    since = total = 0
    for name, tool_input in tool_uses(transcript_path):
        if is_handoff(name, tool_input):
            since = 0
        elif name in EDIT_TOOLS:
            since += 1
            total += 1
    return since, total


def decide(event, state, config, now):
    """Returns the line to show, or None."""
    if event.get("stop_hook_active"):
        return None
    every = config.get("handoff_after_edits") or 0
    if not every:
        return None
    edits, total = edit_counts(event.get("transcript_path"))
    new_since_reminder = total - state.get("reminded_at_total", 0)
    if edits < every or new_since_reminder < every:
        return None
    minutes = (now - state.get("start", now)) / 60
    if minutes < (config.get("handoff_after_minutes") or 0):
        return None
    state["reminded_at_total"] = total
    return (
        f"Handoff reminder: {edits} file edits since the last handoff. Before you stop, run the "
        "handoff skill so decisions and next steps are not left only in this chat."
    )


def main():
    try:
        event = json.load(sys.stdin)
    except ValueError:
        event = {}
    try:
        now = time.time()
        cap_state = read_json(session_file("cap", event.get("session_id")))
        path = session_file("handoff", event.get("session_id"))
        state = {"start": cap_state.get("start", now), **read_json(path)}
        line = decide(event, state, load_config(), now)
        write_json(path, state)
    except Exception:  # noqa: BLE001 - a broken reminder must stay silent
        return 0
    if line:
        print(json.dumps({"systemMessage": line}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
