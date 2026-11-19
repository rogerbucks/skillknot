#!/usr/bin/env python3
"""Sets this clone's commit identity in a cloud agent session, so check.py --history passes.

Usage: python3 scripts/session_setup.py
Writes: `user.name` and `user.email` in this clone's own .git/config, and nothing else

Cloud agent sessions start with a vendor email that check.py rejects, and a commit made with it
can only be fixed by rewriting history. This runs at the start of each Claude Code session in this
repo, through .claude/settings.json. It acts only in a cloud session (CLAUDE_CODE_REMOTE=true), and
only when the email is not already a GitHub noreply address, so a person's own machine is left
alone. It prints nothing and always exits 0, so it can never stop a session from starting.
"""

import os
import subprocess
import sys

OWNER = "rogerbucks"
OWNER_EMAIL = "264575592+rogerbucks@users.noreply.github.com"
NOREPLY = "@users.noreply.github.com"


def git(*args):
    done = subprocess.run(
        ["git", *args], capture_output=True, text=True, timeout=10, check=False
    )
    return done.returncode, done.stdout.strip()


def needs_setup(env, email):
    return env.get("CLAUDE_CODE_REMOTE") == "true" and not email.endswith(NOREPLY)


def main(env=None, runner=git):
    env = os.environ if env is None else env
    try:
        _, email = runner("config", "user.email")
        if needs_setup(env, email):
            runner("config", "--local", "user.name", OWNER)
            runner("config", "--local", "user.email", OWNER_EMAIL)
    except (OSError, subprocess.SubprocessError):
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
