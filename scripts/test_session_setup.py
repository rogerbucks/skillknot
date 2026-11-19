import unittest

import session_setup

OWN = "https://github.com/rogerbucks/skillknot"


class FakeGit:
    def __init__(self, email, origin=OWN):
        self.email = email
        self.origin = origin
        self.calls = []

    def __call__(self, *args):
        self.calls.append(args)
        if args[:2] == ("remote", "get-url"):
            return 0, self.origin
        return 0, self.email

    def wrote(self):
        return [c for c in self.calls if "--local" in c]


CLOUD = {"CLAUDE_CODE_REMOTE": "true"}


class SessionSetupTest(unittest.TestCase):
    def test_cloud_session_with_vendor_email_gets_owner_noreply(self):
        git = FakeGit("noreply@anthropic.com")
        session_setup.main(CLOUD, git)
        self.assertIn(
            ("config", "--local", "user.email", session_setup.OWNER_EMAIL), git.calls
        )
        self.assertIn(("config", "--local", "user.name", "rogerbucks"), git.calls)

    def test_dot_git_origin_counts_as_the_owner_repo(self):
        git = FakeGit(
            "noreply@anthropic.com", "https://github.com/rogerbucks/skillknot.git"
        )
        session_setup.main(CLOUD, git)
        self.assertEqual(len(git.wrote()), 2)

    def test_fork_is_left_alone(self):
        git = FakeGit("noreply@anthropic.com", "https://github.com/someone/skillknot")
        session_setup.main(CLOUD, git)
        self.assertEqual(git.wrote(), [])

    def test_lookalike_repo_is_left_alone(self):
        git = FakeGit(
            "noreply@anthropic.com", "https://github.com/rogerbucks/skillknot-fork"
        )
        session_setup.main(CLOUD, git)
        self.assertEqual(git.wrote(), [])

    def test_noreply_email_is_left_alone(self):
        git = FakeGit("1+someone@users.noreply.github.com")
        session_setup.main(CLOUD, git)
        self.assertEqual(git.wrote(), [])

    def test_local_machine_is_left_alone(self):
        git = FakeGit("person@example.org")
        session_setup.main({}, git)
        self.assertEqual(git.wrote(), [])

    def test_git_failure_never_raises(self):
        def broken(*args):
            raise OSError("no git")

        self.assertEqual(session_setup.main(CLOUD, broken), 0)


if __name__ == "__main__":
    unittest.main()
