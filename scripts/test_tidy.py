"""Tests for tidy.py. Run from the repo root: python3 -m unittest discover -s scripts"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import tidy


class TidyTextTests(unittest.TestCase):
    def test_clean_text_is_unchanged(self):
        self.assertEqual(tidy.tidy_text("a.md", "Plain.\n"), "Plain.\n")

    def test_windows_line_endings_become_unix(self):
        self.assertEqual(tidy.tidy_text("a.md", "a\r\nb\r\n"), "a\nb\n")

    def test_trailing_spaces_go(self):
        self.assertEqual(tidy.tidy_text("a.md", "a  \nb\t\n"), "a\nb\n")

    def test_file_ends_in_one_newline(self):
        self.assertEqual(tidy.tidy_text("a.md", "a"), "a\n")
        self.assertEqual(tidy.tidy_text("a.md", "a\n\n\n"), "a\n")

    def test_empty_file_stays_empty(self):
        self.assertEqual(tidy.tidy_text("a.md", ""), "")

    def test_json_gets_one_layout(self):
        self.assertEqual(tidy.tidy_text("a.json", '{"a":1}'), '{\n  "a": 1\n}\n')

    def test_broken_json_is_left_for_the_checks(self):
        self.assertEqual(tidy.tidy_text("a.json", "{oops}\n"), "{oops}\n")

    def test_curly_quotes_in_a_skill_go_straight(self):
        text = "“It’s”\n"
        self.assertEqual(
            tidy.tidy_text("plugins/a/skills/a/SKILL.md", text), '"It\'s"\n'
        )

    def test_no_break_space_in_a_skill_becomes_a_space(self):
        self.assertEqual(
            tidy.tidy_text("plugins/a/skills/a/SKILL.md", "a b\n"), "a b\n"
        )

    def test_curly_quotes_outside_a_skill_stay(self):
        self.assertEqual(tidy.tidy_text("README.md", "“a”\n"), "“a”\n")


class TidyFilesTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_check_mode_changes_nothing(self):
        path = self.root / "a.md"
        path.write_text("a  \n", encoding="utf-8")
        self.assertEqual(tidy.tidy_files(self.root, ["a.md"], fix=False), ["a.md"])
        self.assertEqual(path.read_text(encoding="utf-8"), "a  \n")

    def test_fix_mode_rewrites_the_file(self):
        path = self.root / "a.md"
        path.write_text("a  \n", encoding="utf-8")
        self.assertEqual(tidy.tidy_files(self.root, ["a.md"], fix=True), ["a.md"])
        self.assertEqual(path.read_text(encoding="utf-8"), "a\n")

    def test_binary_files_are_skipped(self):
        (self.root / "a.png").write_bytes(b"\x89PNG\xff\xfe")
        self.assertEqual(tidy.tidy_files(self.root, ["a.png"], fix=True), [])

    def test_fixed_json_still_parses(self):
        path = self.root / "a.json"
        path.write_text('{"b":[1,2]}', encoding="utf-8")
        tidy.tidy_files(self.root, ["a.json"], fix=True)
        self.assertEqual(json.loads(path.read_text(encoding="utf-8")), {"b": [1, 2]})


if __name__ == "__main__":
    unittest.main()
