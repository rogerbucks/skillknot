"""Tests for the private-words scan script. Run from the repo root: python3 -m unittest discover -s scripts"""

import contextlib
import io
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SKILL = (
    Path(__file__).parent.parent
    / "plugins"
    / "private-words"
    / "skills"
    / "private-words"
    / "scripts"
)
sys.path.insert(0, str(SKILL))
import scan


def git(root, *args):
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)


class WordListTests(unittest.TestCase):
    def test_markdown_takes_only_bullets(self):
        text = "---\nname: x\n- not this\n---\n\n# Title\n\nProse.\n\n- acme\n- beta gamma\n"
        self.assertEqual(scan.parse_words("a.md", text), ["acme", "beta gamma"])

    def test_plain_file_takes_lines_and_skips_comments(self):
        self.assertEqual(
            scan.parse_words("a.txt", "# note\n\nacme\n  beta  \n"), ["acme", "beta"]
        )

    def test_named_list_wins(self):
        self.assertEqual(scan.list_path("/a/b.md"), Path("/a/b.md"))

    def test_environment_comes_next(self):
        with mock.patch.dict(os.environ, {"SKILLKNOT_TERMS_FILE": "/c/d.md"}):
            self.assertEqual(scan.list_path(None), Path("/c/d.md"))

    def test_default_location_comes_last(self):
        with (
            mock.patch.dict(os.environ, {}, clear=True),
            mock.patch.object(Path, "home", return_value=Path("/h")),
        ):
            self.assertEqual(
                scan.list_path(None), Path("/h/.config/skillknot/blocked-terms.md")
            )

    def test_star_bullets_count(self):
        self.assertEqual(scan.parse_words("a.md", "* acme\n"), ["acme"])


class RepoTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name).resolve()
        self.repo = self.base / "repo"
        self.repo.mkdir()
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.name", "x")
        git(self.repo, "config", "user.email", "x@example.com")
        git(self.repo, "config", "commit.gpgsign", "false")
        self.words = self.base / "words.md"
        self.words.write_text("# Mine\n\n- acme\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def add(self, name, text):
        (self.repo / name).write_text(text, encoding="utf-8")
        git(self.repo, "add", ".")

    def run_main(self, *args):
        out, err = io.StringIO(), io.StringIO()
        argv = ["scan.py", "--list", str(self.words), "--repo", str(self.repo), *args]
        with (
            mock.patch.object(sys, "argv", argv),
            contextlib.redirect_stdout(out),
            contextlib.redirect_stderr(err),
        ):
            code = scan.main()
        return code, out.getvalue() + err.getvalue()

    def test_clean_repo_passes(self):
        self.add("a.md", "Nothing here.\n")
        self.assertEqual(self.run_main()[0], 0)

    def test_word_in_a_file_is_found_with_its_line(self):
        self.add("a.md", "one\nAsk ACME\n")
        code, text = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("a.md:2", text)

    def test_word_in_a_file_name_is_found(self):
        self.add("acme-notes.md", "Nothing.\n")
        code, text = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("***-notes.md", text)
        self.assertNotIn("acme", text)

    def test_file_name_is_masked_on_a_line_hit(self):
        self.add("ACME-notes.md", "Ask acme\n")
        code, text = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("***-notes.md:1", text)
        self.assertNotIn("acme", text.lower())

    def test_untracked_file_is_found(self):
        (self.repo / "new.md").write_text("acme\n", encoding="utf-8")
        self.assertEqual(self.run_main()[0], 1)

    def test_output_never_holds_the_word(self):
        self.add("a.md", "Ask acme\n")
        self.assertNotIn("acme", self.run_main()[1])

    def test_allowed_word_is_exempt(self):
        self.add("a.md", "acmecorp\n")
        self.assertEqual(self.run_main("--allow", "acmecorp")[0], 0)

    def test_commit_message_needs_history(self):
        self.add("a.md", "Fine.\n")
        git(self.repo, "commit", "-qm", "Fix the acme thing")
        self.assertEqual(self.run_main()[0], 0)
        self.assertEqual(self.run_main("--history")[0], 1)

    def test_author_name_is_read_in_history(self):
        self.add("a.md", "Fine.\n")
        git(self.repo, "-c", "user.name=acme", "commit", "-qm", "c")
        self.assertEqual(self.run_main("--history")[0], 1)

    def test_author_email_is_read_in_history(self):
        self.add("a.md", "Fine.\n")
        git(self.repo, "-c", "user.email=acme@example.com", "commit", "-qm", "c")
        self.assertEqual(self.run_main("--history")[0], 1)

    def test_a_word_removed_from_a_file_is_found_in_history(self):
        self.add("a.md", "acme\n")
        git(self.repo, "commit", "-qm", "one")
        self.add("a.md", "Fine.\n")
        git(self.repo, "commit", "-qm", "two")
        self.assertEqual(self.run_main()[0], 0)
        code, text = self.run_main("--history")
        self.assertEqual(code, 1)
        self.assertIn("in a file it changed", text)
        self.assertNotIn("acme", text)

    def test_a_folder_that_is_not_a_repo_cannot_run(self):
        self.repo = self.base / "plain"
        self.repo.mkdir()
        code, text = self.run_main("--history")
        self.assertEqual(code, 2)
        self.assertIn("could not run", text)

    def test_where_gives_the_path_and_count_and_no_word(self):
        code, text = self.run_main("--where")
        self.assertEqual(code, 0)
        self.assertIn(str(self.words), text)
        self.assertIn("1 word(s)", text)
        self.assertNotIn("acme", text)

    def test_where_still_gives_the_path_of_a_missing_list(self):
        self.words = self.base / "gone.md"
        code, text = self.run_main("--where")
        self.assertEqual(code, 2)
        self.assertIn(str(self.words), text)

    def test_a_failed_secret_store_cannot_run(self):
        real = subprocess.run

        def fail_gh(command, **kwargs):
            if command[0] == "gh":
                raise FileNotFoundError("gh")
            return real(command, **kwargs)

        with mock.patch.object(scan.subprocess, "run", side_effect=fail_gh):
            self.assertEqual(self.run_main("--set-secret", "LEAK_TERMS")[0], 2)

    def test_list_inside_a_git_repo_is_refused(self):
        self.words = self.repo / "words.md"
        self.words.write_text("- acme\n", encoding="utf-8")
        self.assertEqual(self.run_main()[0], 2)

    def test_missing_list_is_refused(self):
        self.words = self.base / "gone.md"
        self.assertEqual(self.run_main()[0], 2)

    def test_empty_list_is_refused(self):
        self.words.write_text("# Nothing yet\n", encoding="utf-8")
        self.assertEqual(self.run_main()[0], 2)

    def test_secret_goes_by_standard_input_and_is_never_printed(self):
        with mock.patch.object(scan.subprocess, "run") as run:
            run.return_value = subprocess.CompletedProcess([], 0, stdout="false")
            code, text = self.run_main("--set-secret", "LEAK_TERMS")
        self.assertEqual(code, 0)
        self.assertEqual(run.call_args.args[0], ["gh", "secret", "set", "LEAK_TERMS"])
        self.assertEqual(run.call_args.kwargs["input"], "acme\n")
        self.assertNotIn("acme", text)


if __name__ == "__main__":
    unittest.main()
