---
name: claude-code-session-meter
description: Use when setting up or tuning a Claude Code status line that shows branch, unpushed work, context used, cost and time, or a cap that warns when a session runs too long or costs too much, or when the session cap has warned or held a prompt.
license: MIT
compatibility: Claude Code only. Needs python3 (standard library only), and git on the PATH for the branch part. Cost and context come from Claude Code's status line data, which is an estimate, not a bill.
---

# claude-code-session-meter: see the session, cap the session

Two parts, which work alone or together:

| Part | Shows or does | Why it earns its place |
| --- | --- | --- |
| **Status line** | `⎇ main ↑2 ●3 │ ctx 42% │ $1.23 of $5.00 │ 37m │ guards on` | Unpushed commits, a filling context and a growing bill are invisible until they hurt. One glance shows all of them |
| **Session cap** | Warns at 80% and at 100% of a limit on cost, minutes or prompts. Can hold one prompt at the limit | A long session gets slower, costlier and less accurate. A nudge at the right moment saves more than any setting |

Reading the status line, left to right:

- **`⎇ main ↑2 ●3`:** the branch, 2 commits not pushed, 3 files changed. `(not pushed)` means the
  branch has no upstream yet
- **`ctx 42%`:** how full the context window is. `⚠` from 80%: compact or start fresh soon
- **`$1.23 of $5.00`:** estimated session cost, and the cap if one is set
- **`37m`:** time since the session started
- **`guards on`:** the `claude-code-guards` plugin is installed and none is turned off. Nothing
  shown means the meter could not tell. It never means safe

## Install

```bash
claude plugin marketplace add rogerbucks/skillknot
claude plugin install claude-code-session-meter@skillknot
```

**The cap is a hook, so it starts in the next session.** The status line is a setting, which a
plugin cannot set, so it takes one more step:

1. **Copy the two scripts** somewhere stable. They are in the installed plugin's `scripts`
   folder. Find it with `find ~/.claude/plugins -name statusline.py -path '*session-meter*'`,
   then copy `statusline.py` and `meterlib.py` to `~/.claude/skillknot-meter/`
2. **Add this to `~/.claude/settings.json`:**

   ```json
   "statusLine": {
     "type": "command",
     "command": "python3 ~/.claude/skillknot-meter/statusline.py"
   }
   ```

3. **Check it:** the line appears after the next reply. If it does not, run the command in the
   copied folder with `echo '{}' |` in front. It should print a line, not an error

Copy the scripts again after an update to pick up changes.

## Set the limits: the personal overlay

Optional JSON at `~/.config/skillknot/claude-code-session-meter.json`. It stays on your machine.

```json
{
  "max_usd": 5,
  "max_minutes": 120,
  "max_turns": 100,
  "warn_at": 0.8,
  "hard_stop": false
}
```

- **Defaults:** 120 minutes and 100 prompts. No cost cap, because a fair one depends on the plan
  you pay for. Set `null` to turn a limit off
- **`max_usd` needs the status line,** because only the status line is told the cost. Without
  it, the cap counts prompts and minutes only
- **`hard_stop`:** the first prompt past a limit is held, with the reason. Send it again to go on.
  It is held once per limit, so it can never trap you

## When the cap warns you, as the agent

- **Finish the step in hand,** then tell the person in one line which limit passed
- **Offer a way out:** wrap up, run a handoff, or start a fresh session with a short brief
- **Never work faster or cut checks to beat the cap.** The cap is about the person's budget, not
  a race

## Limits, said plainly

- **Cost is Claude Code's own estimate** at list price, and it resets when `/clear` starts a new
  session. It can differ from the bill
- **Readings are a step behind:** the status line updates after each reply, so the cap sees the
  cost as of the last reply
- **Each session keeps two small JSON files in the system temp folder,** named by a hash of the
  session id. The operating system clears them

Sources and design notes: [references/sources.md](references/sources.md).
