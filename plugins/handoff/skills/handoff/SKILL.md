---
name: handoff
description: Use when the user is finishing, wrapping up or closing a working session, asks whether it is safe to stop, or before a long gap in the work. Sweeps the conversation for decisions, findings, next steps and open questions still only in chat, writes them where they belong, releases anything held, cleans up test files, and reports what the next session should pick up.
license: MIT
compatibility: Works with any agent that can read and write the user's files or notes. Needs no scripts. Reads an optional personal file for where things are kept.
---

# handoff: end a session with nothing left only in the chat

**The chat window is not storage.** Decisions usually get written down. What gets lost is the
**recommendations and next steps**, because they live in the conversation and end with it.
**The tasks you write are the handoff.**

**Before step 0, read the project's own rules, then the personal overlay at
`~/.config/skillknot/handoff.md` if it exists.** Those name where decisions, tasks and notes go,
and any checker to run. Without them, ask the user once where tasks and decisions live, and
offer a sensible default: a `decisions/` and a `tasks/` folder in the project.

```text
0 Scope -> 1 Sweep -> 2 Filter -> 3 Mark the source -> 4 Release -> 5 Clean up -> 6 Verify -> 7 Report
```

## 0. Name the scope, and stay inside it

**Report only on the work this session touched.** Write the scope down first, and say it in the
report so the user can correct it in one word:

> *Scope: billing migration, release notes. Tasks outside these are not reported.*

- **The scope comes from what was read or written,** plus anything the user named in chat
- **Unscoped is a bug, not a safe default.** A list of every open task in the project buries the
  two that follow from today. A list nobody can act on teaches the reader to skip the handoff
- **Widen only when asked.** A whole-project review is a different job
- **Scope filters what you report, never what you write.** A decision about a barely touched
  topic is still written down in step 1

## 1. Sweep the session

Read back over the conversation and pull out everything that exists only in chat:

| What came out | Where it goes |
|---|---|
| **A decision:** a choice made, with the options turned down | A decision record, **with what was rejected and why**. One file per decision |
| **A finding:** something now known that was not | The note or document it concerns, dated |
| **A next step or recommendation** | **A task: one task, one file** or one tracker item. A checkbox line is a step inside a task, never a task |
| **An open question** | A task tagged as a question. A deliberate wait is not a question: name what it waits for |
| **Something deliberately dropped** | Say so in the report. Silence reads as forgotten |

**Record a reversal as a reversal.** Never quietly overwrite the decision it replaces. The old
reasoning is what stops the question coming back.

**If a file is generated from other files, write your part to its source,** never to the
roll-up. Hand-edits to a generated file are lost on the next build.

## 2. Filter hard

The way this fails is **writing everything**, which buries the signal. Most of a conversation is
working-out. Write an item only if it passes all three:

1. **Would it still matter in a month?** Superseded attempts and fixed mistakes do not
2. **Is it missing from the records now?** Check first. A near-duplicate is worse than nothing,
   because two places will soon disagree
3. **Does it have a home?** If nothing owns it, resolve that, rather than inventing a note

When unsure, add **one line to an existing note** rather than a new note.

## 3. Mark where each item came from

**The user must tell "the agent suggested this" from "I decided this" at a glance.** Group new
items under a dated heading, or add a short "suggested in session, <date>" clause. Unmarked
suggestions piling up as tasks is how a task list stops being trusted.

**Size each task by one test:** could a fresh session, holding nothing but this task, pick it up
and finish it? Yes: it is a task. Too big: split it. A checklist past about ten steps was sized
wrong. Give each task a **stable identifier** if the system has one, and **what blocks it**.

## 4. Release what you hold

A session that ends still holding a claim parks the work with nobody on it.

- **Release your own locks, leases or "in progress" marks** if the work landed
- **If it did not land, leave the claim and say so,** with where you got to
- **Never release someone else's claim,** whatever its expiry says

## 5. Clean up this session's test files

Testing against real files is good practice, and it leaves throwaways behind.

- **List what you created only to prove something worked,** and say the list before removing any
- **Check that nothing links to a file before removing it.** A test file that is now cited as
  evidence stays
- **Move to the trash or an archive. Never delete outright** unless the user says so
- **If unsure, keep it and say so.** A stray file costs a line in the report. A deleted piece of
  evidence costs the evidence

## 6. Verify

Run the project's own checker if it has one: tests, a link checker, a lint, or the script named
in the overlay. **Run it last,** because a clean check on an unswept session is false comfort.

- **A checker reports, it does not decide.** Do not "fix" a long list of outstanding items just to
  get a clean report
- **If something is genuinely broken, fix it before you finish,** unless another session owns
  it. Then record that it is in flight and whose it is, and say the red light is not yours

## 7. Report honestly

Lead with what the user reads first:

- **The scope**, in one line
- **The next tasks, as a bullet list, one task per bullet, identifier first,** each with what
  finishing it would unblock. Say plainly when a task unblocks nothing. **Never shorten an
  identifier,** because a shortened one cannot be searched for
- **What you wrote, and where,** as links
- **What you deliberately left,** named as choices. Say they are written down and undecided,
  not about to be lost
- **What is waiting on someone else,** with dates
- **One recommendation** for what to do next, not a menu

**Never claim more than was done.** If a step was skipped, say so. The user will trust this
report when they come back and cannot remember.

Sources: [references/sources.md](references/sources.md).
