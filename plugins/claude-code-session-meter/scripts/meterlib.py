"""Shared helpers for the session meter: the overlay, and the small per-session files that let the
status line hand its last reading to the cap.

Usage: imported by statusline.py and session_cap.py beside it.
Writes: nothing itself. The callers write JSON files in the system temp folder, named by a hash of
the session id, so no session id or path appears in a file name.

The overlay is optional JSON at ~/.config/skillknot/claude-code-session-meter.json, for example:
  {"max_usd": 5, "max_minutes": 120, "max_turns": 100, "warn_at": 0.8, "hard_stop": false}
"""

import hashlib
import json
import os
import tempfile
from pathlib import Path

OVERLAY = Path.home() / ".config" / "skillknot" / "claude-code-session-meter.json"
DEFAULTS = {
    "max_usd": None,
    "max_minutes": 120,
    "max_turns": 100,
    "warn_at": 0.8,
    "hard_stop": False,
}


def load_config():
    """The overlay merged over the defaults. A missing or broken overlay gives the defaults."""
    target = Path(os.environ.get("SKILLKNOT_METER_CONFIG", OVERLAY))
    try:
        mine = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        mine = {}
    return {**DEFAULTS, **(mine if isinstance(mine, dict) else {})}


def session_file(kind, session_id):
    digest = hashlib.sha256((session_id or "none").encode()).hexdigest()[:16]
    return Path(tempfile.gettempdir()) / f"skillknot-meter-{kind}-{digest}.json"


def read_json(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def write_json(path, data):
    """Writes through a temporary file, so a reader never sees half a file."""
    path = Path(path)
    spare = path.with_suffix(".tmp")
    spare.write_text(json.dumps(data), encoding="utf-8")
    os.replace(spare, path)
