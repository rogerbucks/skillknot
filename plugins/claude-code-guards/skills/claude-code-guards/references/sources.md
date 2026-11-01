# Where this design comes from

These guards were written fresh for this repo from patterns proven in one person's private agent
setup. No code was copied. The links were read on 1 Nov 2026.

- **[Claude Code hooks](https://code.claude.com/docs/en/hooks).** PreToolUse hooks, and the
  `permissionDecision` answer of `allow`, `ask` or `deny` that each guard returns
- **[Claude Code settings](https://code.claude.com/docs/en/settings) and
  [permissions](https://code.claude.com/docs/en/permissions).** The keys in the hardened
  template: `sandbox`, `permissions.defaultMode`, `permissions.disableBypassPermissionsMode`,
  `enableAllProjectMcpServers`, and the allow, ask and deny rule forms

## Design choices

- **Ask, rather than refuse, wherever a person can judge.** A push is the person's call. The
  guard's job is to show them what they are approving
- **Refuse secret paths outright,** because reading a key cannot be undone
- **A failing guard asks.** A crash must never wave a call through unseen
- **Findings never print a secret.** They name the rule that matched
- **The connector rule targets prompt injection.** Read content can carry instructions, so text
  read from messages should not leave without a person seeing the call
