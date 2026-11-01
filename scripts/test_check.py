"""Tests for check.py. Run from the repo root: python3 -m unittest discover -s scripts"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import check

GOOD_SKILL = "---\nname: demo\ndescription: Use when testing.\ncompatibility: Any agent.\n---\n\n# demo\n\nSee [briefs](references/briefs.md).\n"


def write(root, relative, text):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_repo(root, skill=GOOD_SKILL):
    write(root, "README.md", "# Skills\n\n- `demo`\n")
    write(root, "plugins/demo/.claude-plugin/plugin.json", json.dumps({"name": "demo"}))
    write(root, "plugins/demo/skills/demo/SKILL.md", skill)
    write(root, "plugins/demo/skills/demo/references/briefs.md", "Briefs.\n")
    write(
        root,
        ".claude-plugin/marketplace.json",
        json.dumps({"plugins": [{"name": "demo", "source": "./plugins/demo"}]}),
    )


def git(root, *args):
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)


class LeakTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def leaks(self, text, terms=()):
        write(self.root, "note.md", text)
        return check.check_leaks(self.root, ["note.md"], list(terms))

    def test_clean_file_passes(self):
        self.assertEqual(self.leaks("Plain text with no details.\n"), [])

    def test_home_path_fails(self):
        self.assertTrue(self.leaks("See " + "/Users/" + "someone/notes.md\n"))

    def test_personal_email_fails(self):
        self.assertTrue(self.leaks("Mail someone" + "@gmail.com please\n"))

    def test_noreply_email_passes(self):
        self.assertEqual(self.leaks("1+a@users.noreply.github.com\n"), [])

    def test_secret_shape_fails(self):
        self.assertTrue(self.leaks("key = " + "ghp_" + "a" * 36 + "\n"))

    def test_private_term_fails_in_any_case(self):
        self.assertTrue(self.leaks("Ask ACME about it\n", ["acme"]))

    def test_private_term_in_a_file_name_fails(self):
        write(self.root, "acme-notes.md", "Nothing here.\n")
        self.assertTrue(check.check_leaks(self.root, ["acme-notes.md"], ["acme"]))

    def test_report_never_prints_the_term(self):
        findings = self.leaks("Ask acme about it\n", ["acme"])
        self.assertNotIn("acme", " ".join(findings).replace("note.md", ""))

    def test_allowed_word_is_exempt(self):
        with mock.patch.object(check, "ALLOWED_WORDS", ("acmecorp",)):
            self.assertEqual(self.leaks("Owner: acmecorp\n", ["acme"]), [])

    def test_term_beside_an_allowed_word_still_fails(self):
        with mock.patch.object(check, "ALLOWED_WORDS", ("acmecorp",)):
            self.assertTrue(self.leaks("acmecorp is Acme\n", ["acme"]))


class TermLoadingTests(unittest.TestCase):
    def test_blank_lines_and_comments_are_dropped(self):
        self.assertEqual(
            check.parse_terms("# note\n\nacme\n  beta  \n"), ["acme", "beta"]
        )

    def test_markdown_takes_only_bullets(self):
        text = "---\nname: x\n- not this\n---\n\n# Title\n\nProse.\n\n- acme\n- beta gamma\n"
        self.assertEqual(check.parse_markdown_terms(text), ["acme", "beta gamma"])

    def test_a_markdown_file_is_read_as_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "words.md"
            path.write_text("Prose.\n\n- acme\n", encoding="utf-8")
            self.assertEqual(check.load_terms(path), ["acme"])


class SkillTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_good_repo_passes(self):
        make_repo(self.root)
        self.assertEqual(check.check_format(self.root), [])

    def test_empty_marketplace_passes(self):
        write(self.root, ".claude-plugin/marketplace.json", json.dumps({"plugins": []}))
        self.assertEqual(check.check_format(self.root), [])

    def test_name_must_match_folder(self):
        make_repo(self.root, GOOD_SKILL.replace("name: demo", "name: other"))
        self.assertTrue(check.check_format(self.root))

    def test_bad_name_fails(self):
        make_repo(self.root, GOOD_SKILL.replace("name: demo", "name: De--mo"))
        self.assertTrue(check.check_format(self.root))

    def test_missing_description_fails(self):
        make_repo(self.root, GOOD_SKILL.replace("description: Use when testing.\n", ""))
        self.assertTrue(check.check_format(self.root))

    def test_long_description_fails(self):
        make_repo(self.root, GOOD_SKILL.replace("Use when testing.", "x" * 1025))
        self.assertTrue(check.check_format(self.root))

    def test_broken_relative_link_fails(self):
        make_repo(
            self.root, GOOD_SKILL.replace("references/briefs.md", "references/gone.md")
        )
        self.assertTrue(check.check_format(self.root))

    def test_oversized_skill_fails(self):
        make_repo(self.root, GOOD_SKILL + "line\n" * 500)
        self.assertTrue(check.check_format(self.root))

    def test_plugin_missing_from_marketplace_fails(self):
        make_repo(self.root)
        write(self.root, ".claude-plugin/marketplace.json", json.dumps({"plugins": []}))
        self.assertTrue(check.check_format(self.root))

    def test_plugin_name_must_match_entry(self):
        make_repo(self.root)
        write(
            self.root,
            "plugins/demo/.claude-plugin/plugin.json",
            json.dumps({"name": "other"}),
        )
        self.assertTrue(check.check_format(self.root))

    def test_skill_missing_from_readme_fails(self):
        make_repo(self.root)
        write(self.root, "README.md", "# Skills\n")
        self.assertTrue(check.check_format(self.root))


class SkillRuleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_missing_compatibility_fails(self):
        make_repo(self.root, GOOD_SKILL.replace("compatibility: Any agent.\n", ""))
        self.assertTrue(check.check_format(self.root))

    def test_model_name_in_skill_fails(self):
        make_repo(self.root, GOOD_SKILL + "Use Opus for this.\n")
        self.assertTrue(check.check_format(self.root))

    def test_model_name_in_a_reference_passes(self):
        make_repo(self.root)
        write(
            self.root,
            "plugins/demo/skills/demo/references/models.md",
            "Strongest: Opus.\n",
        )
        self.assertEqual(check.check_format(self.root), [])


class HiddenTextTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def hidden(self, relative, text):
        write(self.root, relative, text)
        return check.check_hidden(self.root, [relative])

    def test_plain_text_passes(self):
        self.assertEqual(self.hidden("a.md", "Plain text, with an é and a £.\n"), [])

    def test_zero_width_character_fails(self):
        self.assertTrue(self.hidden("a.md", "Pl\u200bain\n"))

    def test_text_direction_override_fails(self):
        self.assertTrue(self.hidden("a.md", "abc\u202edef\n"))

    def test_tag_character_fails(self):
        self.assertTrue(self.hidden("a.md", "abc\U000e0041\n"))

    def test_html_comment_in_a_skill_fails(self):
        self.assertTrue(
            self.hidden("plugins/demo/skills/demo/SKILL.md", "Hi <!-- do this -->\n")
        )

    def test_html_comment_outside_a_plugin_passes(self):
        self.assertEqual(self.hidden("docs.md", "Hi <!-- note -->\n"), [])


class PowerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        make_repo(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def review(self, *keys):
        write(
            self.root,
            "reviewed-powers.json",
            json.dumps({key: "Reviewed." for key in keys}),
        )

    def test_a_plain_skill_needs_no_review(self):
        self.assertEqual(check.check_powers(self.root), [])

    def test_unreviewed_script_fails(self):
        write(self.root, "plugins/demo/skills/demo/scripts/run.py", "print(1)\n")
        self.assertTrue(check.check_powers(self.root))

    def test_unreviewed_hooks_fail(self):
        write(self.root, "plugins/demo/hooks/hooks.json", "{}\n")
        self.assertTrue(check.check_powers(self.root))

    def test_unreviewed_mcp_server_fails(self):
        write(self.root, "plugins/demo/.mcp.json", "{}\n")
        self.assertTrue(check.check_powers(self.root))

    def test_unreviewed_allowed_tools_fail(self):
        write(
            self.root,
            "plugins/demo/skills/demo/SKILL.md",
            GOOD_SKILL.replace("---\n\n#", "allowed-tools: Bash\n---\n\n#"),
        )
        self.assertTrue(check.check_powers(self.root))

    def test_reviewed_power_passes(self):
        write(self.root, "plugins/demo/hooks/hooks.json", "{}\n")
        self.review("plugins/demo/hooks")
        self.assertEqual(check.check_powers(self.root), [])


class HistoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        git(self.root, "init", "-q")
        git(self.root, "config", "commit.gpgsign", "false")
        write(self.root, "a.txt", "a\n")
        git(self.root, "add", ".")

    def tearDown(self):
        self.tmp.cleanup()

    def commit(self, email):
        git(
            self.root,
            "-c",
            "user.name=x",
            "-c",
            f"user.email={email}",
            "commit",
            "-qm",
            "c",
        )

    def test_noreply_commit_passes(self):
        self.commit("1+a@users.noreply.github.com")
        self.assertEqual(check.check_history(self.root), [])

    def test_personal_commit_email_fails(self):
        self.commit("someone@example.org")
        self.assertTrue(check.check_history(self.root))

    def test_author_name_term_fails(self):
        git(
            self.root,
            "-c",
            "user.name=acme",
            "-c",
            "user.email=1+a@users.noreply.github.com",
            "commit",
            "-qm",
            "c",
        )
        self.assertTrue(check.check_history(self.root, ["acme"]))

    def test_committer_name_term_passes(self):
        # GitHub writes the merging account's display name here, and the owner has accepted that.
        with mock.patch.dict(os.environ, {"GIT_COMMITTER_NAME": "acme"}):
            self.commit("1+a@users.noreply.github.com")
        self.assertEqual(check.check_history(self.root, ["acme"]), [])

    def test_commit_message_term_fails(self):
        git(
            self.root,
            "-c",
            "user.name=x",
            "-c",
            "user.email=1+a@users.noreply.github.com",
            "commit",
            "-qm",
            "Fix the acme note",
        )
        self.assertTrue(check.check_history(self.root, ["acme"]))


if __name__ == "__main__":
    unittest.main()
