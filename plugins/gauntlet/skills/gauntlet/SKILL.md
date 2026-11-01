---
name: gauntlet
description: Use when the user names an existing item to improve against a bar with a Gauntlet Loop or Gauntlet Run, types /gauntlet with an item, or asks for repeated builder and critic rounds, a blind A/B against a reference, or a capped multi-agent quality pass on a page, script, report or document.
license: MIT
compatibility: Needs an agent harness with subagents, such as Claude Code. Model names are Claude tiers, so map them to your own.
---

# gauntlet: improve one named item against a bar, inside a cap

**The item is whatever the user names.** This file supplies the stages, the models and the stop
rules. Agent briefs are in [references/briefs.md](references/briefs.md): read it at Stage 2. The
evidence behind the design is in [references/sources.md](references/sources.md).

**Before Stage 0, read the project's own rules, then the personal overlay at
`~/.config/skillknot/gauntlet.md` if it exists.** Those rules may name folders, guards and
models, and may tighten any rule here. They never remove a gate or the final critic.

```text
0 Fit -> 1 Plan and bar -> GATE: user -> 2 Fixed items -> 3 First version -> 4 Scripts
  -> 5 Loop weak pieces -> 6 Final critic -> 7 Results -> GATE: user -> 8 Swap
```

**Every stage runs, in this order.** A small item gets small stages. A stage with nothing to do
is named in the plan with the reason. The final critic always runs.

## Stage 0: Fit check

All three must be true:

- **Inspectable:** the output can be measured or seen, such as a page, a running script, test
  results, or a document against a rubric
- **Reference:** a named exemplar exists, or an answer key can be written
- **Worth it:** better quality is worth more than the cap

**If any is false, this skill stops.** Say which test failed, and do the job with one good prompt
and one review. **Writing sent in a person's own voice always fails the test,** because that
person is the only judge of it.

## Stage 1: Plan and bar

**Before the gate, only read, measure and write the plan.** No backup, agent or build yet.

Write `.gauntlet/<item-slug>/plan.md` at the project root, or beside the item if it has no
project, and keep `.gauntlet/` out of version control. The plan goes in this order:

1. **The ask**, and the item's exact paths
2. **Baseline:** counts measured by a script now, before anything changes
3. **The bar:** a machine bar (a script that exits 0) and a judged bar (a named reference, with
   what the judge looks for). With no reference, write an answer key: the correct outcomes,
   agreed with the user at the gate. Critics may not change the bar
4. **Pieces:** the smallest separately judged parts. Mark each *fixed* (fully specified, so no
   judgement is needed), *coupled* (a change affects another piece) or *independent*
5. **Where things live** (below), checked against the project's guards before the first agent
6. **Cap and stop rules**, and an estimate per stage, including the lead session
7. **The capture or test tool**, and how it will be proved

Ask the user only what the bar cannot be written without. If told not to ask, make the choice,
mark it in the plan, and show it at the gate.

**Then stop for one yes on the bar and cap.** A request that names a specific reference, its pass
criteria and a cap already is that yes, so show the plan and carry on, unless the cap cannot pay
for the plan. "Make it great", "just start" and "go" are not a yes: they approve speed, not a bar
nobody has seen. Show the bar and wait for one word.

**For a document or data file,** the capture is the content itself, the machine bar is a script
over it (links, section lengths, reading level, recalculated totals), and the bar lists what the
judge scores.

### Where things live

- **Code in a Git repo:** a new branch. Replacing the live item at Stage 8 is the merge, behind
  the repo's checks
- **Anything else:** a working copy in `.gauntlet/<item-slug>/work/`, which stays out of version
  control
- **Plan, captures, pairs and results:** `.gauntlet/<item-slug>/`
- **Backup:** a dated copy of the live item, after the yes and before any agent. A branch needs none
- **Live item:** untouched until Stage 8

### Models

- **Haiku:** fixed, fully specified edits, one pass, outside the loop. Never a critic or judge
- **Sonnet:** builders and round critics
- **Opus:** blind judges and the final critic. If asked for Opus builders, plan Sonnet and say at
  the gate that one pilot found over three times Sonnet's cost for the same result. Opus builds
  only if the user repeats the ask
- **Lead session:** budget about a third of the cap
- **Local models:** builders at most, never critics or judges

### Cap and stop rules

- **Default cap:** $20 (estimate). Caps are what the tokens would cost at API prices, even on a
  flat-rate plan. One pilot, three design rounds on three reports, cost about $15
- **Small cap:** reserve a third for the lead and a fifth for the final critic. What is left pays
  for pieces and rounds. If it cannot pay for a loop, offer two things at the gate: a higher cap,
  or one pass plus the final critic and no loop
- **Per piece:** at most 3 rounds, and stop after 2 with no win
- **Plan usage:** if the harness shows usage limits, check before each round and start no new
  round past 70% of the current window
- **Agents:** coupled pieces one at a time, otherwise at most 4 alive, at most 1 on Opus

## Stages 2 to 4: Fixed items, first version, scripts

- **2 Fixed items:** one Haiku pass
- **3 First version:** one Sonnet pass per piece, no critic, in dependency order
- **4 Scripts:** run the machine bar after each piece. Failures go back to the same builder, at
  most twice. Read the checker's result yourself. A checker can be wrong, so count a sample by
  hand once

## Stage 5: Loop weak pieces only

**A weak piece** is one that still falls short of the judged bar after Stage 4. **Prove the capture tool first:** capture something whose result you already know. For a page,
use a real browser at true widths and in both colour modes.

Each round:

1. **Critic:** a new Sonnet agent, given the bar and real captures, never the builder's reasoning
2. **Blind pair:** you make an unlabelled pair of the best version and this round's (see the
   briefs), and a new Opus agent gives the verdict without knowing which is which
3. **Ratchet:** keep the round only if it beats the best so far. Otherwise restore the best
4. **Next round:** the same builder fixes the judge's named faults, on the kept version

**A round is void** if its capture is faulty or a measurement came from the builder alone.

## Stage 6: Final critic

A new Opus agent reads the whole item at every width, mode and state, with the bar. Fix its
blockers, rerun the machine bar, and say which fixes had no blind judgement. If the verdict is
*Hold* (not *Ship*), the item stays out, and that is a result.

## Stage 7: Results

- **Tally** model, tokens and cost per piece and round, including the lead session, from the
  token counts your tools report. Label it an estimate
- **Write** the result into the plan
- **Show the user** before and after, what passed, what did not, and what was never verified
- **Stop.** Replacing the live item is the user's call

## Stage 8: Swap, after the user's yes

Back up again if the live item has changed. Remove any lines added only for the run, replace the live item (or
merge the branch), rerun the machine bar on the live item, and render it once. Note in the plan
what now stands in its place.

## Rules for every run

- **Every agent brief carries the guard line:** if a guard blocks an action, stop and report it.
  Never reword, re-encode or use another tool to get around it
- **Keep the bar stable,** so repeated reads stay cheap and nothing drifts
- **A finding the bar missed** goes to the user as a change to the bar, with the reason
- **Keep `.gauntlet/<item-slug>/status.md` current,** so a person can see the run and stop it
