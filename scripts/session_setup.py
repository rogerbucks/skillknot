#!/usr/bin/env python3
"""Sets this clone's commit identity in a cloud agent session, so check.py --history passes.

Usage: python3 scripts/session_setup.py
Writes: `user.name` and `user.email` in this clone's own .git/config, and nothing else

Cloud agent sessions start with a vendor email that check.py rejects, and a commit made with it
can only be fixed by rewriting history. This runs at the start of each Claude Code session in this
repo, through .claude/settings.json. It acts only in a cloud session (CLAUDE_CODE_REMOTE=true),
only when origin is the owner's own repo (a fork or another clone is left alone), and only when the
email is not already one that check.py accepts, so a person's own machine is left alone. It prints nothing and always exits 0, so it can never stop a session from starting.
"""

import os
import re
import subprocess
import sys

OWNER = "rogerbucks"
OWNER_EMAIL = "264575592+rogerbucks@users.noreply.github.com"
# The same addresses check.py --history accepts.
NOREPLY = re.compile(r"(@users\.noreply\.github\.com|^noreply@github\.com)$")
# github.com/<owner>/<repo>, over https or ssh, with or without .git
ORIGIN = re.compile(r"github\.com[:/]rogerbucks/skillknot(\.git)?/?$")


def git(*args):
    done = subprocess.run(
        ["git", *args], capture_output=True, text=True, timeout=10, check=False
    )
    return done.returncode, done.stdout.strip()


def needs_setup(env, origin, email):
    return (
        env.get("CLAUDE_CODE_REMOTE") == "true"
        and ORIGIN.search(origin) is not None
        and NOREPLY.search(email) is None
    )


def main(env=None, runner=git):
    env = os.environ if env is None else env
    try:
        _, origin = runner("remote", "get-url", "origin")
        _, email = runner("config", "user.email")
        if needs_setup(env, origin, email):
            runner("config", "--local", "user.name", OWNER)
            runner("config", "--local", "user.email", OWNER_EMAIL)
    except (OSError, subprocess.SubprocessError):
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
