---
name: design-brief
description: Use before designing or building anything from a loose request - a page, screen, form, document, report, process, workflow or tool - when the user says "make me a", "design a", "can you build", or the goal, audience or finish line is unclear. Turns the ask into a one-page brief (audience, the job it does, limits, what is out, and a test of done) and gets one yes before work starts.
license: MIT
compatibility: Works with any agent. Needs no tools. Produces a short Markdown brief.
---

# design-brief: agree what good looks like before building

**Most rework comes from building the wrong thing well.** A vague ask hides three or four
different jobs, and each builder guesses a different one. Ten minutes on a brief saves the
rebuild.

**Read the personal overlay at `~/.config/skillknot/design-brief.md` if it exists.** It may name
house styles, brand rules, accessibility levels or audiences you design for often.

**Skip the brief when the ask is already specific,** or small enough to redo in less time than a
brief takes. Say you skipped it and why, in one line.

```text
1 Restate -> 2 Fill gaps -> 3 Write the brief -> 4 One yes -> 5 Build against it
```

## 1. Restate the ask in one sentence

*"You want a one-page form that lets new suppliers register, so finance stops chasing details by
email."* If you cannot write this sentence, the ask is not clear yet. That is the first
question.

## 2. Fill the gaps, and guess first

Ask only about what is missing, in one message, **each with your best guess** so the user can
just say yes:

| Gap | Ask | Example guess |
| --- | --- | --- |
| **Who uses it** | Who, how often, on what device, with what skill? | "Supplier admin staff, once each, mostly on a laptop" |
| **The job** | What should they be able to do, or decide, that they cannot today? | "Register in under 5 minutes without calling us" |
| **Success** | How will we know it worked? | "Fewer than 1 in 10 forms come back incomplete" |
| **Limits** | Brand, platform, budget, deadline, rules, accessibility? | "Our brand colours; must meet accessibility level AA" |
| **Out of scope** | What will it not do? | "No payment set-up; that stays in the finance system" |

Never ask more than five questions. If the user says "you decide", use your guesses and say so in
the brief.

## 3. Write the brief: one page, no more

```markdown
# Brief: supplier registration form

**Job:** let a new supplier register in under 5 minutes without calling us
**For:** supplier admin staff; once each; mostly laptop; varied English
**Success:** fewer than 1 in 10 forms need follow-up (today: about 4 in 10)
**Must:** brand colours; accessibility level AA; works on a phone too
**Won't:** set up payments; replace the finance system
**Risks:** bank details are sensitive, so the form must not email them
**Test of done:** three people who have never seen it complete it unaided
**Assumed:** the guesses marked (guess) above, unless you correct them
```

Rules:

- **The job is an outcome for a person,** not a feature list. "Register without calling us", not
  "a form with 14 fields"
- **The test of done is something you can watch or measure.** "Looks professional" is not a test
- **"Won't" is as important as "must".** It stops scope from creeping in during the build
- **Mark every guess as a guess,** so the user can see what they have not confirmed

## 4. Get one yes

Show the brief and ask for one answer: *"Build to this?"* Change what they correct, then go. Do
not ask again for small changes. Note them in the brief and carry on.

## 5. Build against the brief, and check against it

- **Keep the brief beside the work** and re-read the job line when choosing between options
- **If a planning panel is available** (the `planning-panel` skill or its pane), fill it as the
  brief takes shape: Job as the goal, For as the audience, Must and Won't as limits, gaps as open
  questions
- **When a new idea appears mid-build,** check it against "won't". If it does not fit, note it as
  a later idea instead of adding it
- **At the end, run the test of done** or say plainly that it has not been run yet, and how to

## Design habits worth applying in any build

- **One main action per screen or page.** Make it obvious; demote the rest
- **Use the user's words,** not the organisation's internal names
- **Show the state:** what happened, what is next, and what went wrong in plain words
- **Design for the worst case first:** a slow connection, a small screen, a tired reader
- **Accessible by default:** enough contrast, labels on every field, works with a keyboard

Sources and design notes: [references/sources.md](references/sources.md).
