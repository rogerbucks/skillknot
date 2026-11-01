#!/usr/bin/env python3
"""Keeps the skillknot plugins in Claude Code current, on each push to the repo's main branch.

Usage: python3 scripts/autoupdate.py [--install-launchd | --uninstall-launchd] [--force]
Writes: the last commit it installed and a short log, in ~/.local/state/skillknot. With
--install-launchd, also a copy of itself in ~/.local/share/skillknot and one launchd job file

Each run asks GitHub for the newest commit on main, which is one small request. If main has not
moved since the last run, it stops there. If it has, it refreshes the skillknot marketplace,
updates every installed skillknot plugin and installs any skillknot plugin that is not installed
yet. It only runs `claude plugin` commands for the skillknot marketplace, so other plugins,
marketplaces and settings stay as they are.

--install-launchd (macOS) runs it at login and every 15 minutes. The job runs a copy of this file,
not the repo's, so a later push never changes what runs on the machine without a person copying it.
"""

import argparse
import json
import os
import plistlib
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO = "rogerbucks/skillknot"
MARKETPLACE = "skillknot"
LABEL = "io.github.rogerbucks.skillknot.autoupdate"
INTERVAL_SECONDS = 900
LOG_LINES = 500
STATE = Path.home() / ".local" / "state" / "skillknot"
SHARE = Path.home() / ".local" / "share" / "skillknot"
AGENT_FILE = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"


def run(command, timeout=300):
    """Runs one command with no input and returns (exit code, output)."""
    try:
        done = subprocess.run(
            command,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as problem:
        return 1, str(problem)
    return done.returncode, (done.stdout + done.stderr).strip()


def latest_commit(runner=run):
    code, out = runner(
        ["git", "ls-remote", f"https://github.com/{REPO}.git", "refs/heads/main"],
        timeout=60,
    )
    if code != 0 or not out:
        return None
    sha = out.split()[0]
    return sha if len(sha) == 40 else None


def parse_json(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def has_marketplace(runner=run):
    code, out = runner(["claude", "plugin", "marketplace", "list", "--json"])
    entries = parse_json(out) if code == 0 else None
    return any(entry.get("name") == MARKETPLACE for entry in entries or [])


def plan(listing):
    """Turns `claude plugin list --available --json` into (to install, to update)."""
    suffix = f"@{MARKETPLACE}"
    installed = {
        entry["id"]
        for entry in listing.get("installed", [])
        if entry.get("id", "").endswith(suffix)
    }
    available = sorted(
        entry["pluginId"]
        for entry in listing.get("available", [])
        if entry.get("marketplaceName") == MARKETPLACE and "pluginId" in entry
    )
    return [p for p in available if p not in installed], sorted(installed)


def update(runner=run, log=print):
    """Refreshes the marketplace and its plugins. Returns True if the marketplace step worked."""
    if not has_marketplace(runner):
        code, out = runner(["claude", "plugin", "marketplace", "add", REPO])
        if code != 0:
            log(f"could not add the marketplace: {out[-300:]}")
            return False
        log("added the skillknot marketplace")
    code, out = runner(["claude", "plugin", "marketplace", "update", MARKETPLACE])
    if code != 0:
        log(f"could not refresh the marketplace: {out[-300:]}")
        return False
    code, out = runner(["claude", "plugin", "list", "--available", "--json"])
    listing = parse_json(out) if code == 0 else None
    if not isinstance(listing, dict):
        log("could not read the plugin list")
        return False
    to_install, to_update = plan(listing)
    failed = []
    for action, plugins in (("install", to_install), ("update", to_update)):
        for plugin in plugins:
            code, out = runner(["claude", "plugin", action, plugin])
            if code != 0:
                failed.append(plugin)
                log(f"{action} {plugin} failed: {out[-300:]}")
    log(
        f"installed {len(to_install)}, checked {len(to_update)} for updates, "
        f"{len(failed)} failed"
    )
    return True


def write_log(line):
    STATE.mkdir(parents=True, exist_ok=True)
    path = STATE / "autoupdate.log"
    old = path.read_text().splitlines() if path.exists() else []
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    path.write_text("\n".join([*old, f"{stamp} {line}"][-LOG_LINES:]) + "\n")


def check_and_update(force=False, runner=run, log=write_log):
    last = STATE / "last-commit"
    sha = latest_commit(runner)
    if sha is None:
        log("could not reach GitHub, will try again next run")
        return 0
    if not force and last.exists() and last.read_text().strip() == sha:
        return 0
    log(f"main is now {sha[:12]}")
    if not update(runner, log):
        return 1
    STATE.mkdir(parents=True, exist_ok=True)
    last.write_text(sha + "\n")
    return 0


def agent_plist(program, path_value):
    """Returns the launchd job file. plistlib escapes every value."""
    job = {
        "Label": LABEL,
        "ProgramArguments": program,
        "EnvironmentVariables": {"PATH": path_value},
        "RunAtLoad": True,
        "StartInterval": INTERVAL_SECONDS,
        "ProcessType": "Background",
    }
    return plistlib.dumps(job).decode()


def install_launchd():
    claude = shutil.which("claude")
    if sys.platform != "darwin" or claude is None:
        print("This needs macOS with the claude command on PATH.")
        return 1
    SHARE.mkdir(parents=True, exist_ok=True)
    copy = SHARE / "autoupdate.py"
    shutil.copyfile(__file__, copy)
    path_value = os.pathsep.join(
        dict.fromkeys([str(Path(claude).parent), *os.environ["PATH"].split(os.pathsep)])
    )
    AGENT_FILE.parent.mkdir(parents=True, exist_ok=True)
    AGENT_FILE.write_text(agent_plist([sys.executable, str(copy)], path_value))
    domain = f"gui/{os.getuid()}"
    run(["launchctl", "bootout", domain, str(AGENT_FILE)])
    code, out = run(["launchctl", "bootstrap", domain, str(AGENT_FILE)])
    if code != 0:
        print(f"launchctl refused the job: {out}")
        return 1
    print(
        f"Installed. It runs now, then every 15 minutes. Log: {STATE / 'autoupdate.log'}"
    )
    return 0


def uninstall_launchd():
    run(["launchctl", "bootout", f"gui/{os.getuid()}", str(AGENT_FILE)])
    for path in (AGENT_FILE, SHARE / "autoupdate.py"):
        path.unlink(missing_ok=True)
    print("Removed the job. Installed plugins stay as they are.")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--install-launchd", action="store_true")
    group.add_argument("--uninstall-launchd", action="store_true")
    parser.add_argument(
        "--force", action="store_true", help="update even if main has not moved"
    )
    args = parser.parse_args(argv)
    if args.install_launchd:
        return install_launchd()
    if args.uninstall_launchd:
        return uninstall_launchd()
    return check_and_update(force=args.force)


if __name__ == "__main__":
    sys.exit(main())
