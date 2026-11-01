---
name: context-budget
description: Use when an agent session feels slow or heavy, after editing always-loaded instructions (CLAUDE.md, AGENTS.md, rules files), after adding a skill or hook, or for a regular check. Measures the context loaded on every turn, hook latency and rule-index drift against stated budgets, and fixes a breach by moving material to where it loads on demand, never by quietly deleting it.
license: MIT
compatibility: Works with any agent that loads instruction files and can run shell commands. Token counts are estimates, not exact.
---

# context-budget: keep the setup fast by measuring, not believing

Every setup creeps. The always-loaded instructions gain a section per decision. A rule is added
without its index. A hook gets slower. None of it shows until a session feels sluggish, and by
then nobody can tell which change caused it.

**Read the project's own rules, then the personal overlay at
`~/.config/skillknot/context-budget.md` if it exists.** It may set the files to measure, the
budgets, and where results are recorded.

## What to measure, and the starting budgets

| Measure | What it is | Starting budget |
| --- | --- | --- |
| **Always-loaded context** | Every instruction file read on every turn: the main agent file, imported files, output style | 13,000 tokens |
| **Session-start context** | What is read once per session: indexes, memory, start-up hook output | 22,000 tokens |
| **Per-turn hook time** | All hooks that run on every turn or stop, added up | 3 seconds |
| **Rules against index** | Every numbered or named rule appears in its index, and the index lists nothing extra | Zero drift |
| **Skills: source against installed** | Installed copies match their source | Zero drift |

**Estimate tokens as characters divided by about 3.8.** The absolute number is rough. **The
change between runs carries the signal,** and a stable estimator keeps that change honest. Never
quote these figures as exact.

## How to measure

```bash
wc -c AGENTS.md CLAUDE.md .claude/rules/*.md 2>/dev/null        # always-loaded size, in characters
time (echo '{}' | <each per-turn hook command> >/dev/null)      # hook time, one at a time
```

Save each run's numbers with the date, so the next run can show the change.

## When to run

| Trigger | Run |
| --- | --- |
| **After editing always-loaded instructions** | Everything. These are the numbers you just changed |
| **After adding or changing a hook** | Everything. Latency is the point |
| **After adding a rule or a skill** | Index and drift checks |
| **A session feels slow** | Everything, before theorising |
| **Weekly** | Everything, and record the result somewhere visible |

## Fix a breach by relocating, never by deleting

**A budget is breached or it is not. There is no score,** because a score invites optimising
the score.

- **Always-loaded context over budget:** keep each rule's one line, and move its reasoning,
  measurements and rejected options into a linked decision record. A recurring procedure becomes
  a skill, which loads on demand. A reference table becomes a linked note
- **Session-start context over budget:** index it, and load the detail on demand
- **Hook time over budget:** find the slowest hook and ask whether its output changes every
  turn. If not, run it only when its inputs change
- **Index drift:** fix it now, in the same session. It is usually one line, and drift means a
  session reads an index that silently omits a rule
- **Skill drift:** reinstall from source

**If a fact would be lost, it has not been optimised. It has been dropped,** which is a different
decision and needs the user's sign-off.

## After a run

- **A breach with an obvious fix:** fix it, and say so
- **A breach without one:** a task, with the number in it
- **A breach you accept:** record the decision and why, so the next run does not reopen it
- **Record every run where it is visible,** so a check that stops running shows as overdue
  rather than silently absent

Sources: [references/sources.md](references/sources.md).
