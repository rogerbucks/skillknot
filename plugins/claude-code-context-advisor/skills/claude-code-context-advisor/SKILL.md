---
name: claude-code-context-advisor
description: Use when a Claude Code session feels slow, costly or forgetful, when the user asks how full the context is, whether to compact or start fresh, what is using up the context, or how to make sessions cheaper. Reads the session's own record and reports big files read in full when a section would do, files read again unchanged, heavy tool output, how full the context is, and where a subagent or a cheaper model would have done. Advises only; changes nothing.
license: MIT
compatibility: Claude Code only, because it reads Claude Code's session records. Needs python3 (standard library only). Token figures are estimates.
---

# claude-code-context-advisor: spend context on purpose

**Context is the agent's working memory, and it fills up.** Every file read and every command
output stays in it until the session is compacted or ends. A full context costs more per reply,
answers more slowly and forgets the start of the session. Most of it is lost to a few habits:
reading whole files, reading them twice, and letting commands print far more than needed.

**This reads the record and says what to change.** It never edits, deletes or compacts anything.

| It finds | Why it matters | What to do instead |
| --- | --- | --- |
| **A big file read in full** (over ~8,000 tokens) | Most of it was never needed, and it stays for the rest of the session | Search first, then read only the lines you need |
| **A file read again with no edit between** | The first copy is still in context, so the second is pure cost | Refer back to the first read |
| **Heavy tool output** (over ~10,000 tokens) | A long log or listing crowds out the work | Filter at the source: a narrower search, `head`, a quiet flag |
| **A long run of searches** (15 or more with no edit) | Exploring fills the context with dead ends | Hand the search to a research subagent, which returns only the answer |
| **Mostly routine steps** | Lookups do not need the strongest model | Give them to a cheaper model or a subagent. The `model-picker` skill shows how to test that |
| **How full the context is** | Past 60% it is time to plan; past 80% it is time to act | Compact at a natural break, or hand off and start fresh |

## Run it

The script is in this skill's `scripts` folder:

```bash
python3 scripts/advise.py --latest            # the newest session for this folder
python3 scripts/advise.py --latest --window 1000000   # for a model with a larger context
python3 scripts/advise.py path/to/session.jsonl       # one session record
```

Claude Code keeps session records under `~/.claude/projects/`, one folder per project folder.
`--latest` finds the newest one for the current folder. Add `--json` for output another tool can
read.

## When you are the agent and the user asks for this

1. **Run the script** with `--latest`, and the user's context size if they gave one
2. **Lead with the verdict:** how full the context is, and whether to compact, hand off or carry on
3. **Give the top three findings** in one line each, with what to do differently. Skip the rest
   unless asked
4. **Change your own habits for the rest of the session,** such as reading by section. Say once
   that you are doing so
5. **Do not compact, clear or start a new session yourself.** Offer it, and let the user choose.
   Before either, offer the `handoff` skill so nothing is lost

## Good habits, whatever the report says

- **Search, then read the section.** A search shows where to look; a full read is the last resort
- **Ask for less output:** limit lines, filter logs, use summary flags
- **Send exploring to a subagent,** so only the conclusion comes back into the main session
- **Compact at a break, not mid-task.** A summary taken mid-change loses the detail you need next
- **Start fresh for a new task.** Old context is noise for new work

## Limits, said plainly

- **Token counts are estimates,** about 4 characters to a token. The context figure uses the last
  reply's own counts when the record has them
- **Only the main session is read.** Subagent work is in their own context and not counted here
- **The record format belongs to Claude Code** and can change. If the report looks empty or odd,
  check that the record is a current one before trusting it
- **The report shows file names and sizes, never contents.** Paths can still be private, so share
  it with care

Sources and design notes: [references/sources.md](references/sources.md).
