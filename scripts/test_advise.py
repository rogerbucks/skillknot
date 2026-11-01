"""Tests for the claude-code-context-advisor script. Run: python3 -m unittest discover -s scripts"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parent.parent
    / "plugins"
    / "claude-code-context-advisor"
    / "skills"
    / "claude-code-context-advisor"
    / "scripts"
    / "advise.py"
)


def call(n, name, data):
    return {
        "type": "assistant",
        "message": {
            "content": [
                {"type": "tool_use", "id": f"t{n}", "name": name, "input": data}
            ]
        },
    }


def result(n, chars):
    return {
        "type": "user",
        "message": {
            "content": [
                {"type": "tool_result", "tool_use_id": f"t{n}", "content": "x" * chars}
            ]
        },
    }


class Advise(unittest.TestCase):
    def run_on(self, records, *extra):
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as handle:
            for record in records:
                handle.write(json.dumps(record) + "\n")
        done = subprocess.run(
            [sys.executable, str(SCRIPT), handle.name, "--json", *extra],
            capture_output=True,
            text=True,
            check=True,
        )
        Path(handle.name).unlink()
        return json.loads(done.stdout)

    def kinds(self, out):
        return [f["kind"] for f in out["findings"]]

    def test_findings(self):
        records = [
            call(1, "Read", {"file_path": "/p/big.md"}),
            result(1, 40_000),
            call(2, "Read", {"file_path": "/p/big.md", "offset": 1, "limit": 50}),
            result(2, 2_000),
            call(3, "Read", {"file_path": "/p/a.py"}),
            result(3, 4_000),
            call(4, "Read", {"file_path": "/p/a.py"}),
            result(4, 4_000),
            call(5, "Edit", {"file_path": "/p/a.py"}),
            result(5, 10),
            call(6, "Read", {"file_path": "/p/a.py"}),
            result(6, 4_000),
            call(7, "Bash", {"command": "pytest -v"}),
            result(7, 60_000),
            {
                "type": "assistant",
                "message": {
                    "content": [],
                    "usage": {
                        "input_tokens": 10,
                        "cache_read_input_tokens": 150_000,
                        "cache_creation_input_tokens": 20_000,
                    },
                },
            },
        ]
        out = self.run_on(records)
        kinds = self.kinds(out)
        self.assertEqual(kinds.count("Big file read in full"), 1)
        repeat = [f for f in out["findings"] if f["kind"] == "Read again, unchanged"]
        a_py = [f for f in repeat if "/p/a.py" in f["detail"]]
        self.assertEqual(len(a_py), 1)
        self.assertEqual(a_py[0]["tokens"], 1_000)
        self.assertIn("Heavy tool output", kinds)
        self.assertEqual(kinds[0], "Heavy tool output")
        self.assertEqual(out["context_tokens"], 170_010)
        self.assertIn("80%", out["advice"])
        self.assertIn("room", self.run_on(records, "--window", "1000000")["advice"])

    def test_compaction_resets_and_search_runs(self):
        records = [call(1, "Read", {"file_path": "/p/big.md"}), result(1, 40_000)]
        records.append({"type": "system", "subtype": "compact_boundary"})
        for n in range(2, 20):
            records += [call(n, "Grep", {"pattern": "x"}), result(n, 100)]
        out = self.run_on(records)
        self.assertNotIn("Big file read in full", self.kinds(out))
        self.assertIn("Long search run", self.kinds(out))
        self.assertEqual(out["compactions"], 1)
        self.assertIsNone(out["context_tokens"])

    def test_sidechains_and_bad_lines_are_skipped(self):
        side = call(1, "Read", {"file_path": "/p/big.md"})
        side["isSidechain"] = True
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as handle:
            handle.write(
                "not json\n"
                + json.dumps(side)
                + "\n"
                + json.dumps(result(1, 40_000))
                + "\n"
            )
        done = subprocess.run(
            [sys.executable, str(SCRIPT), handle.name],
            capture_output=True,
            text=True,
            check=True,
        )
        Path(handle.name).unlink()
        self.assertIn("Nothing to fix", done.stdout)


if __name__ == "__main__":
    unittest.main()
