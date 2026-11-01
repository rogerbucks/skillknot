#!/usr/bin/env python3
"""Warns when a Claude Code session passes its limits on prompts, minutes or cost, and can stop
one prompt so the person decides on purpose whether to go on.

Usage: a UserPromptSubmit hook (see ../hooks/hooks.json). To try it by hand:
  echo '{"session_id":"t","prompt":"hi"}' | python3 session_cap.py
Writes: one small JSON file per session in the system temp folder, holding the start time, the
prompt count and which warnings were already given.

Cost comes from the status line's last reading, because only the status line is told the cost.
Without the status line, the cap still counts prompts and minutes. Each warning is given once.
With "hard_stop": true, the first prompt past a limit is stopped. Sending it again goes through.
"""

import json
import sys
import time

from meterlib import load_config, read_json, session_file, write_json

LIMITS = (
    ("max_usd", "usd", "cost", lambda v: f"${v:.2f}"),
    ("max_minutes", "minutes", "time", lambda v: f"{int(v)} minutes"),
    ("max_turns", "turns", "prompts", lambda v: f"{int(v)} prompts"),
)


def measures(state, reading):
    minutes = reading.get("minutes") or (time.time() - state["start"]) / 60
    return {"usd": reading.get("usd"), "minutes": minutes, "turns": state["turns"]}


def check(state, reading, config):
    """Returns (warnings for the person, a note for the agent, a reason to stop the prompt)."""
    now = measures(state, reading)
    warnings, stop = [], None
    note = None
    warn_at = config.get("warn_at") or 0.8
    for key, measure, label, show in LIMITS:
        limit, value = config.get(key), now[measure]
        if not limit or value is None:
            continue
        ratio = value / limit
        if ratio >= 1 and f"{measure}:full" not in state["warned"]:
            state["warned"].append(f"{measure}:full")
            warnings.append(
                f"Session cap: {label} has passed its limit, {show(value)} of {show(limit)}."
            )
            note = (
                f"The session has passed its {label} limit. Finish the current step, then suggest "
                "the person wraps up or starts a fresh session, and offer a handoff."
            )
            if config.get("hard_stop") and measure not in state["stopped"]:
                state["stopped"].append(measure)
                stop = (
                    f"Session cap: {label} is at {show(value)}, past the limit of {show(limit)}. "
                    "This prompt was held so you can decide. Send it again to go on, or raise the "
                    "limit in ~/.config/skillknot/claude-code-session-meter.json."
                )
        elif warn_at <= ratio < 1 and f"{measure}:near" not in state["warned"]:
            state["warned"].append(f"{measure}:near")
            warnings.append(
                f"Session cap: {label} is at {int(ratio * 100)}% of its limit ({show(value)} of {show(limit)})."
            )
    return warnings, note, stop


def main():
    try:
        event = json.load(sys.stdin)
    except ValueError:
        event = {}
    try:
        session = event.get("session_id")
        path = session_file("cap", session)
        state = {
            "start": time.time(),
            "turns": 0,
            "warned": [],
            "stopped": [],
            **read_json(path),
        }
        state["turns"] += 1
        warnings, note, stop = check(
            state, read_json(session_file("reading", session)), load_config()
        )
        write_json(path, state)
    except Exception:  # noqa: BLE001 - a broken meter must never block the person's prompt
        return 0
    if stop:
        print(json.dumps({"decision": "block", "reason": stop}))
    elif warnings:
        out = {"systemMessage": " ".join(warnings)}
        if note:
            out["hookSpecificOutput"] = {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": note,
            }
        print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
