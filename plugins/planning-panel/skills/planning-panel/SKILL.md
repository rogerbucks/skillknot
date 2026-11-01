---
name: planning-panel
description: Use when the user is planning something - a project, document, deck, design, event, trip or decision - and the plan is spread across the chat. Keeps five fields current (goal, audience, limits, open questions, next steps), in a live pane beside the chat where the agent offers one, or as a short plan block in the chat where it does not. Works alongside design-brief and slide-storyline.
license: MIT
compatibility: Works with any agent. The live pane needs Claude Code with early access to mods and this plugin's hooks module installed. Without them the plan stays in the chat.
---

# planning-panel: keep the plan in view while you talk

**Plans get lost in long chats.** The goal shifts, a limit is mentioned once and forgotten, and a
question stays open without anyone noticing. Keeping five fields in view fixes that.

**Read the personal overlay at `~/.config/skillknot/planning-panel.md` if it exists.** It may set
house limits, usual audiences or how often to show the plan.

## The five fields

| Field | Holds | Example |
| --- | --- | --- |
| **Goal** | The job or decision, in one sentence | Pick a venue for the team day |
| **Audience** | Who it is for, or who decides | Twelve people; the manager decides |
| **Limits** | Musts, won'ts, budget, deadline, rules | Under 2,000 in total; step-free access |
| **Open questions** | What is still undecided or unknown | Which date? |
| **Next steps** | The next actions, in order | Shortlist three venues |

Rules:

- **One short plain sentence per item.** The panel is read at a glance
- **A question leaves the list once answered,** and its answer moves into goal, audience or limits
- **Mark guesses as guesses** until the user confirms them
- **Next steps start with a verb** and are things someone can do this week

## Where the plan lives

- **A live pane (Claude Code with mods).** If the `update_plan` tool from this plugin is
  available, call it each time a field changes. Send only the fields that changed: a list you send
  replaces that list whole. Do not repeat the plan in the chat as well, because the pane shows it
- **No pane.** If the tool answers that no pane can show (some app views draw none), or there is
  no tool, show the plan as a short block when it changes in a way that matters: a new goal,
  a new limit, or a question answered. Not after every message

```markdown
**Goal:** Pick a venue for the team day
**Audience:** Twelve people; the manager decides
**Limits:** under 2,000 in total; step-free access
**Open:** Which date?
**Next:** Shortlist three venues
```

## With other skills

- **`design-brief`:** its Job fills Goal, For fills Audience, Must and Won't fill Limits, and its
  gaps fill Open questions. Its test of done becomes the last next step
- **`slide-storyline`:** its frame fills the fields. Who decides is the Audience, what they should
  do after the last slide is the Goal, and length and format are Limits
- **`handoff`:** at the end of a session, the open questions and next steps are what to carry over

## Limits, said plainly

- **The pane shows only what the agent sends.** It does not read the chat by itself
- **The pane lasts for the session.** Use `/plan-panel copy` or the plan block to keep it

Sources and design notes: [references/sources.md](references/sources.md).
