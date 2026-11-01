# Where this design comes from

Written fresh for this repo. No code was copied. The links were read on 1 Nov 2026.

- **[Claude Code status line](https://code.claude.com/docs/en/statusline).** The `statusLine`
  setting, and the JSON it passes on standard input: `cost.total_cost_usd`,
  `cost.total_duration_ms`, `context_window.used_percentage` and `workspace.current_dir`
- **[Claude Code hooks](https://code.claude.com/docs/en/hooks).** The `UserPromptSubmit` event,
  `systemMessage` to warn the person, `additionalContext` to tell the agent, and
  `decision: "block"` to hold a prompt

## Design choices

- **Warn first, stop at most once.** A cap that blocks every prompt traps the person in their own
  session. Holding one prompt makes going on a choice, which is the point
- **The status line hands its reading to the cap,** because hooks are not told the cost
- **No default cost cap.** What a session should cost depends on the plan someone pays for, so
  only the person can set it
- **Unknown is shown as nothing, never as safe.** The guards part appears only when the meter can
  read the plugin list
- **A broken meter stays silent.** It must never block a prompt by failing
