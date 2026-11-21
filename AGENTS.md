# Rules for agents working in this repo

- **This repo is public.** Nothing here may name its owner's life, machines, folders, employers or
  notes. Personal rules belong in `~/.config/skillknot/<skill>.md`, outside the repo
- **Rewrite, never copy.** A skill arrives here as fresh general text, with its sources credited
- **Commit only with a GitHub noreply address,** and keep commit messages free of personal detail
- **Run `python3 scripts/tidy.py`, then `python3 scripts/check.py --history --require-terms`, ruff
  and the tests, before a push.** The pre-push hook runs the check and ruff, through uvx or pipx. Changes
  reach `main` through a pull request that passes CI
- **If a check or guard blocks you, stop and report it.** Never reword or re-encode around it
- **Keep check output free of the private words,** because CI logs are public
- **Keep skills vendor neutral.** One folder per skill, with limits declared in `compatibility` and
  model names only in `references/models.md`. A skill that truly works with one vendor says so in
  its name. The one exception is a subagent's own `model:` line, because the tool needs it there;
  `check.py` refuses a model name anywhere else in an agent file
- **Anything that lets a plugin act needs a line in `reviewed-powers.json`,** saying why it is safe:
  hooks, scripts, agents, commands, MCP servers and `allowed-tools`
- **Dry-run every new skill as a stranger would,** because no check can tell if its advice is good
