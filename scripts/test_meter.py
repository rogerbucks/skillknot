"""Tests for the claude-code-session-meter scripts. Run: python3 -m unittest discover -s scripts"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

METER = (
    Path(__file__).resolve().parent.parent
    / "plugins"
    / "claude-code-session-meter"
    / "scripts"
)


class Meter(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.config = Path(self.tmp.name, "meter.json")
        self.env = {
            **os.environ,
            "TMPDIR": self.tmp.name,
            "HOME": self.tmp.name,
            "SKILLKNOT_METER_CONFIG": str(self.config),
        }

    def tearDown(self):
        self.tmp.cleanup()

    def run_script(self, script, event):
        done = subprocess.run(
            [sys.executable, str(METER / script)],
            input=json.dumps(event),
            capture_output=True,
            text=True,
            env=self.env,
            check=True,
        )
        return done.stdout.strip()

    def cap(self, session="s"):
        out = self.run_script("session_cap.py", {"session_id": session, "prompt": "x"})
        return json.loads(out) if out else None

    def test_status_line(self):
        with tempfile.TemporaryDirectory() as repo:
            subprocess.run(["git", "init", "-q", repo], check=True)
            Path(repo, "a.txt").write_text("a")
            out = self.run_script(
                "statusline.py",
                {
                    "session_id": "s",
                    "workspace": {"current_dir": repo},
                    "cost": {"total_cost_usd": 1.234, "total_duration_ms": 75 * 60000},
                    "context_window": {"used_percentage": 85},
                },
            )
        self.assertIn("●1", out)
        self.assertIn("(not pushed)", out)
        self.assertIn("ctx 85% ⚠", out)
        self.assertIn("$1.23", out)
        self.assertIn("1h15", out)
        empty = {"workspace": {"current_dir": self.tmp.name}}
        self.assertEqual(self.run_script("statusline.py", empty), "")
        plugins = Path(self.tmp.name, ".claude", "plugins")
        plugins.mkdir(parents=True)
        (plugins / "installed_plugins.json").write_text(
            '{"claude-code-guards@skillknot": {}}'
        )
        self.assertEqual(self.run_script("statusline.py", empty), "guards on")

    def test_cap_warns_once_per_level(self):
        self.config.write_text(json.dumps({"max_turns": 5, "max_minutes": None}))
        results = [self.cap() for _ in range(7)]
        self.assertEqual(
            [r is not None for r in results],
            [False, False, False, True, True, False, False],
        )
        self.assertIn("80%", results[3]["systemMessage"])
        self.assertIn("passed its limit", results[4]["systemMessage"])
        self.assertIn("additionalContext", results[4]["hookSpecificOutput"])

    def test_cost_from_status_line_and_hard_stop(self):
        self.config.write_text(
            json.dumps(
                {
                    "max_usd": 2,
                    "max_turns": None,
                    "max_minutes": None,
                    "hard_stop": True,
                }
            )
        )
        self.assertIsNone(self.cap("c"))
        self.run_script(
            "statusline.py", {"session_id": "c", "cost": {"total_cost_usd": 2.5}}
        )
        held = self.cap("c")
        self.assertEqual(held["decision"], "block")
        self.assertIn("$2.50", held["reason"])
        self.assertIsNone(self.cap("c"))

    def test_broken_input_is_silent(self):
        done = subprocess.run(
            [sys.executable, str(METER / "session_cap.py")],
            input="not json",
            capture_output=True,
            text=True,
            env=self.env,
            check=True,
        )
        self.assertEqual(done.stdout, "")


if __name__ == "__main__":
    unittest.main()
