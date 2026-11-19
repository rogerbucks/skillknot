import unittest

import session_setup


class FakeGit:
    def __init__(self, email):
        self.email = email
        self.calls = []

    def __call__(self, *args):
        self.calls.append(args)
        return 0, self.email


class SessionSetupTest(unittest.TestCase):
    def test_cloud_session_with_vendor_email_gets_owner_noreply(self):
        git = FakeGit("noreply@anthropic.com")
        session_setup.main({"CLAUDE_CODE_REMOTE": "true"}, git)
        self.assertIn(
            ("config", "--local", "user.email", session_setup.OWNER_EMAIL), git.calls
        )
        self.assertIn(("config", "--local", "user.name", "rogerbucks"), git.calls)

    def test_noreply_email_is_left_alone(self):
        git = FakeGit("1+someone@users.noreply.github.com")
        session_setup.main({"CLAUDE_CODE_REMOTE": "true"}, git)
        self.assertEqual(git.calls, [("config", "user.email")])

    def test_local_machine_is_left_alone(self):
        git = FakeGit("person@example.org")
        session_setup.main({}, git)
        self.assertEqual(git.calls, [("config", "user.email")])

    def test_git_failure_never_raises(self):
        def broken(*args):
            raise OSError("no git")

        self.assertEqual(session_setup.main({"CLAUDE_CODE_REMOTE": "true"}, broken), 0)


if __name__ == "__main__":
    unittest.main()
