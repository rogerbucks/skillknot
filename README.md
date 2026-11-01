# SkillKnot

SkillKnot is a collection of reusable skills for AI coding agents. Each one is a plain folder in the
[Agent Skills format](https://agentskills.io/specification), packaged here as a Claude Code plugin,
so you can install only the ones you want.

## Skills

- **`gauntlet`:** improve one existing item against a stated bar, inside a spending cap. It uses
  builders, fresh critics and blind judging, and adapts
  [Matt Shumer's Gauntlet Loop](https://somethingbig.ai/gauntlet-loop). The design and its sources
  are in [references/sources.md](plugins/gauntlet/skills/gauntlet/references/sources.md).
  **Status: early.** The method has been piloted by hand, but the skill has not yet had a full run.

## Install

In Claude Code:

```bash
claude plugin marketplace add rogerbucks/skillknot
```

```bash
claude plugin install gauntlet@skillknot
```

Then run it as `/gauntlet:gauntlet <item>`.

For another agent, or to read before you trust it, copy the skill's folder from
`plugins/<name>/skills/<name>` into that agent's skills folder.

## Make it yours

Each skill reads your project's own rules. It also reads a personal file if you have one at
`~/.config/skillknot/<skill>.md`, where you can name your folders, models and guards. That file
stays on your machine, so the skills here can stay general.

## Add a skill

A skill belongs here if it would work, unchanged and useful, for someone else on another machine.

1. Add `plugins/<name>/skills/<name>/SKILL.md` and `plugins/<name>/.claude-plugin/plugin.json`
2. List the plugin in `.claude-plugin/marketplace.json` and the skill above
3. Credit your sources in the skill's `references/sources.md`
4. Run `python3 scripts/check.py`, and open a pull request

`main` takes only changes that pass CI. The check looks for home folder paths, personal email
addresses, secrets and a list of private words kept outside the repo, and it tests each skill's
format. Turn on the same check for your own pushes with `git config core.hooksPath .githooks`.

## Licence

[MIT](LICENSE). Linked sources keep their own licences.
