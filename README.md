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

- **`adversarial-review`:** a hostile expert panel attacks one or more items before they ship. It
  profiles each item's audiences, language style, expectations, standards and legal obligations
  by region and by company lifecycle phase and industry, proposes the experts with reasons for you
  to confirm, always runs any lens you ask for, and cites every finding to a linked source. Default
  registries cover global standards, the US, EU, UK, Australia and New Zealand, Asia Pacific and
  Canada. Each source is a link with a cached note, rechecked when over a week old.
  **Status: early.** Paper design only, no live run yet.

- **`private-words`:** keep private words out of a repo. The list lives only where you choose,
  outside every repo, and a script scans files and history without ever showing a word.

## Install

In Claude Code:

```bash
claude plugin marketplace add rogerbucks/skillknot
```

```bash
claude plugin install <skill>@skillknot
```

Then run it as `/<skill>:<skill>`, for example `/gauntlet:gauntlet <item>`.

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
3. Say what the skill needs in its `compatibility` field
4. Credit your sources in the skill's `references/sources.md`
5. Dry-run it as a stranger would, because no check can tell if its advice is good
6. Run `python3 scripts/check.py`, and open a pull request

`main` takes only changes that pass CI. The check looks for home folder paths, personal email
addresses, secrets, hidden text and a list of private words kept outside the repo, and it tests
each skill's format. Anything that lets a plugin act, such as a hook, a script or a tool permission,
needs a reviewed line in `reviewed-powers.json`. Run `python3 scripts/tidy.py` to fix file layout. `git config core.hooksPath .githooks` runs that
before each commit and the same check before each push.

## Vendors

Skills here stay vendor neutral, with one folder per skill. Each skill declares what it needs in
`compatibility`, and any model names go in its `references/models.md`. A skill that truly works
with one vendor says so in its name.

## Licence

[MIT](LICENSE). Linked sources keep their own licences.
