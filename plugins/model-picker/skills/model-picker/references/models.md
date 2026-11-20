# Model tiers by vendor

The skill names tiers, so it works with any vendor. Model line-ups change often: check the
vendor's own models page before relying on this list, and put your own map in
`~/.config/skillknot/model-picker.md`.

- **Anthropic Claude:** fast Haiku, mid Sonnet, strongest Opus. Effort settings and prompt
  caching are both available as extra dials

**The plugin's Claude Code subagents** pin these in their `model:` field: `scout` on Haiku,
`builder` on Sonnet and `reviewer` on Opus. Claude Code picks a subagent's model in this order:
a model passed on the call, then the agent's `model:`, then the `CLAUDE_CODE_SUBAGENT_MODEL`
setting, then the chat's own model. So a default subagent model never overrides these three.

**Add your vendor here** as one line in the same shape: vendor, then fast, mid and strongest.

**A local model** can take script-like and fast-tier steps when data must stay on the machine.
Test it on the same sample before trusting it.
