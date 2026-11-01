# Install notes

## 1. Add the marketplace

In Claude Code:

```bash
claude plugin marketplace add rogerbucks/skillknot
```

## 2. Install what you want

Each skill is its own plugin, so install only what you need:

```bash
claude plugin install handoff@skillknot
claude plugin install claude-code-guards@skillknot
```

Run a skill as `/<name>:<name>`, or let the agent pick it from its description.

**For another agent,** copy `plugins/<name>/skills/<name>/` into that agent's skills folder. The
Claude Code extras (hooks, the output style, the subagent) do not carry over.

## 3. Add your personal overlay (optional)

Each skill reads `~/.config/skillknot/<skill>.md` if it exists. Put your own folders, names,
voice and rules there. That file stays on your machine, so the skills can stay general.

| Skill | Useful things to put in its overlay |
| --- | --- |
| `handoff` | Where decisions and tasks live, and the checker to run at the end |
| `polish-document` | House style, required frontmatter, where polished files go |
| `document-bundle` | Registry location, audiences, converter |
| `verdict-first` | How to address you, language variant |
| `obsidian-canvas` | Colour scheme, icon vocabulary, node sizes |
| `context-budget` | Files to measure, budgets, where to record runs |

`claude-code-guards` reads JSON instead, at `~/.config/skillknot/claude-code-guards.json`. See
its [skill](../plugins/claude-code-guards/skills/claude-code-guards/SKILL.md).

`claude-code-session-meter` reads JSON too, at
`~/.config/skillknot/claude-code-session-meter.json`, and its status line needs one line in your
settings. See its [skill](../plugins/claude-code-session-meter/skills/claude-code-session-meter/SKILL.md).

## 4. Harden a project's Claude Code settings

1. Copy [settings.hardened.json](../plugins/claude-code-guards/templates/settings.hardened.json)
   to the project's `.claude/settings.json`, or merge its lists into yours
2. Allow the project's own commands by exact form, such as `Bash(npm run test *)`. **Never allow
   an interpreter with `-c`, `-e`, `-` or a bare `*`.** That allows any code
3. Run `/status` to confirm the file loaded, and `claude doctor` if a rule seems ignored

The sandbox is the real boundary. Deny rules on command prefixes only slow mistakes down.

## 5. Check the guards work

In a scratch repo, ask the agent to run `git push`. You should get a prompt that lists the repo,
target, commits and files. Ask it to read `~/.ssh/config`: the secret guard should refuse. Ask it to
run `git reset --hard` there: the destructive check should ask first.

## Contributing

See "Add a skill" in the [README](../README.md). Turn on the local check with
`git config core.hooksPath .githooks`, and keep your private word list at
`~/.config/skillknot/blocked-terms.md`, one word per bullet.
