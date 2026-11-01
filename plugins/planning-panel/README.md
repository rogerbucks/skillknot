# planning-panel

A pane that stays beside the chat in Claude Code and fills in as you plan. It shows five things,
kept current as the conversation moves:

| Field | Holds |
| --- | --- |
| **Goal** | What the plan is for, in one sentence |
| **Audience** | Who it is for, or who decides |
| **Limits** | Musts, won'ts, budget, deadline, rules |
| **Open questions** | What is still undecided |
| **Next steps** | The next actions, in order |

The plan is drawn as a route. The goal sits at the top, each step is a station, and an open
question hangs off the step it holds up. A progress bar and a fence of limits frame it.

| Colour | Means |
| --- | --- |
| **Green** | Done |
| **Blue** | Now: the first step free to start |
| **Amber** | Held by an open question, or a question no step owns yet |
| **Grey** | Later |
| **Red** | A limit |

Desktop, editor and mobile panes draw this as a picture. A drawing cannot read the app's theme,
so it carries its own dark board. The terminal has no vector drawing, so it shows the same route
in coloured text.

> **Early access.** The pane is a Claude Code mod, and mods need Claude Code's early-access
> switch today. Install this plugin only if your Claude Code has that switch on. Without it, use
> the `planning-panel` skill on its own: it keeps the same five fields in the chat instead.

## Install

At the prompt of a terminal session:

```text
/plugin install planning-panel --marketplace rogerbucks/skillknot
```

## Use

- **Start planning.** Claude calls the panel's `update_plan` tool as the goal, audience, limits,
  questions and steps change, and the pane opens the first time it does
- **Tie a question to a step.** A question sent as `{ text, step }` holds that step, counted from
  1, until the question goes. A step sent as `{ text, done: true }` shows as finished
- **`/plan-panel`** opens the pane. **`/plan-panel clear`** empties it. **`/plan-panel copy`**
  prints the plan as Markdown, ready to paste
- **With other skills.** While `design-brief` or `slide-storyline` runs, their answers fill the
  same fields, so the brief or the deck's frame builds up beside the chat

## What it can do

It registers one tool and one command, and draws one pane. It keeps the plan in the session's own
state, which outlives a reload but not the session. It sends nothing anywhere, reads no files and
runs no commands. Each text is capped at 300 characters and each list at 12 items.

## Develop

`claude plugin validate plugins/planning-panel` checks the module, and
`claude plugin test plugins/planning-panel` runs `tests/panel.test.tsx`.
