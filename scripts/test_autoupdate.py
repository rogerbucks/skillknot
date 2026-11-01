import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import autoupdate

SHA = "a" * 40
LISTING = {
    "installed": [
        {"id": "chart-picker@skillknot"},
        {"id": "other@elsewhere"},
    ],
    "available": [
        {"pluginId": "chart-picker@skillknot", "marketplaceName": "skillknot"},
        {"pluginId": "gauntlet@skillknot", "marketplaceName": "skillknot"},
        {"pluginId": "stranger@elsewhere", "marketplaceName": "elsewhere"},
    ],
}


class FakeRunner:
    def __init__(self, fail=()):
        self.calls = []
        self.fail = set(fail)

    def __call__(self, command, timeout=300):
        self.calls.append(command)
        joined = " ".join(command)
        if any(part in joined for part in self.fail):
            return 1, "boom"
        if command[0] == "git":
            return 0, f"{SHA}\trefs/heads/main"
        if command[-2:] == ["list", "--json"]:
            return 0, json.dumps([{"name": "skillknot"}])
        if "--available" in command:
            return 0, json.dumps(LISTING)
        return 0, "ok"


class PlanTest(unittest.TestCase):
    def test_installs_missing_and_updates_installed_only_for_skillknot(self):
        to_install, to_update = autoupdate.plan(LISTING)
        self.assertEqual(to_install, ["gauntlet@skillknot"])
        self.assertEqual(to_update, ["chart-picker@skillknot"])


class CheckAndUpdateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        patcher = mock.patch.object(autoupdate, "STATE", Path(self.tmp.name))
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.tmp.cleanup)
        self.log = []

    def go(self, runner, force=False):
        return autoupdate.check_and_update(force, runner, self.log.append)

    def test_updates_then_skips_when_main_has_not_moved(self):
        runner = FakeRunner()
        self.assertEqual(self.go(runner), 0)
        commands = [" ".join(c) for c in runner.calls]
        self.assertIn("claude plugin install gauntlet@skillknot", commands)
        self.assertIn("claude plugin update chart-picker@skillknot", commands)
        self.assertFalse(any("elsewhere" in c for c in commands))
        again = FakeRunner()
        self.assertEqual(self.go(again), 0)
        self.assertEqual(len(again.calls), 1)

    def test_only_runs_skillknot_plugin_commands(self):
        runner = FakeRunner()
        self.go(runner)
        for command in runner.calls:
            if command[0] == "claude":
                self.assertEqual(command[1], "plugin")
                self.assertTrue(
                    any("skillknot" in part for part in command) or "list" in command
                )

    def test_offline_does_nothing(self):
        runner = FakeRunner(fail=["ls-remote"])
        self.assertEqual(self.go(runner), 0)
        self.assertEqual(len(runner.calls), 1)

    def test_failed_marketplace_refresh_retries_next_run(self):
        self.assertEqual(self.go(FakeRunner(fail=["marketplace update"])), 1)
        self.assertFalse((Path(self.tmp.name) / "last-commit").exists())

    def test_one_failed_plugin_does_not_stop_the_rest(self):
        runner = FakeRunner(fail=["install gauntlet"])
        self.assertEqual(self.go(runner), 0)
        self.assertTrue(any("gauntlet@skillknot failed" in line for line in self.log))
        self.assertIn(
            ["claude", "plugin", "update", "chart-picker@skillknot"], runner.calls
        )

    def test_adds_marketplace_when_missing(self):
        runner = FakeRunner()
        original = runner.__call__

        def no_marketplace(command, timeout=300):
            if command[-2:] == ["list", "--json"]:
                runner.calls.append(command)
                return 0, "[]"
            return original(command, timeout)

        self.go(no_marketplace)
        self.assertIn(
            ["claude", "plugin", "marketplace", "add", "rogerbucks/skillknot"],
            runner.calls,
        )


class PlistTest(unittest.TestCase):
    def test_plist_runs_at_load_every_fifteen_minutes(self):
        text = autoupdate.agent_plist(["/usr/bin/python3", "/x/autoupdate.py"], "/bin")
        self.assertIn("<integer>900</integer>", text)
        self.assertIn("<key>RunAtLoad</key>", text)
        self.assertIn("<string>/x/autoupdate.py</string>", text)


if __name__ == "__main__":
    unittest.main()
