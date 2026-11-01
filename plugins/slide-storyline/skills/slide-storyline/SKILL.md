---
name: slide-storyline
description: Use when the user needs a presentation, deck, board pack, pitch or briefing slides, or wants to turn notes, a report or data into slides. Builds the storyline before any design - one headline claim per slide, evidence beneath it, ordered so a reader who skims only the headlines still gets the argument - then checks it and hands over an outline any slide tool can build.
license: MIT
compatibility: Works with any agent. Produces a Markdown outline. Building the actual slides needs a slide tool or skill, which this does not supply.
---

# slide-storyline: decks that survive a skim

**Most decks fail before design.** They are a pile of topics with labels like "Background" and
"Market", so the reader has to work out the point. Fix the story first. Fonts and colours come
last, and matter least.

**Read the personal overlay at `~/.config/skillknot/slide-storyline.md` if it exists.** It may
set a house template, a slide limit, a tone, or audiences you present to often.

```text
1 Frame -> 2 Answer first -> 3 Headlines -> 4 Evidence -> 5 Skim test -> 6 Hand over
```

## 1. Frame: three questions, asked once

Ask only what you cannot infer. Offer a guess with each, so the user can answer in one word.

| Question | Why it matters |
| --- | --- |
| **Who decides, and what do they already believe?** | A board, a team and a customer need different openings. A sceptic needs the evidence earlier |
| **What should they do or think after the last slide?** | This is the deck's whole job. Without it, every slide is optional |
| **How long, and will it be presented or read?** | A read deck needs full-sentence headlines and no speaker. A spoken deck can lean on the speaker |

If a planning panel is available (the `planning-panel` skill or its pane), keep the answers
there: who decides as the audience, what they should do as the goal, length and format as limits.

## 2. Put the answer first

Write the deck's one-sentence answer before any slide: the recommendation, the finding or the
ask. Then choose an order:

- **Answer, then reasons (the default):** for leaders and busy readers. They get the point in
  ten seconds and read on only if they doubt it
- **Situation, complication, resolution:** when the audience does not yet feel the problem.
  Keep the first two to one slide each
- **Options, then the pick:** only when the decision is genuinely theirs and the options are
  close. Never more than three options

## 3. Write a headline for every slide

**A headline is a claim, not a label.** It is a full sentence the slide then proves.

| Label (avoid) | Claim (use) |
| --- | --- |
| Q3 results | Q3 revenue beat plan by 8%, all of it from renewals |
| Market overview | Two rivals now undercut us on price in our largest segment |
| Next steps | We need a yes on the pilot budget by 15 March |

Rules for headlines:

- **One claim per slide.** Two claims means two slides, or one claim is not needed
- **15 words or fewer,** so the eye takes it in one pass
- **Numbers where they exist,** with the unit and the period
- **Read the headlines alone, in order.** They must tell the whole story. This is the deck

## 4. Put only proof under each headline

- **Each slide's body proves its headline and nothing else.** Move the rest to an appendix
- **One chart or one table or three short points.** Not all three. For charts, use the
  `chart-picker` skill if it is installed
- **Say where each number came from,** in small text at the foot of the slide
- **Put caveats where they bite,** on the slide they affect, not in a footnote at the end

## 5. Run the skim test before handing over

| Check | Pass when |
| --- | --- |
| **Headlines alone** | Read in order, they make the argument with no slide bodies |
| **The ask** | The action and the date appear on the first or second slide and on the last |
| **No orphan slides** | Every slide supports the answer, or it is in the appendix |
| **Length** | About one slide per two minutes spoken, or the user's limit |
| **Numbers** | Every figure has a source and a unit, and none is invented. A gap is marked as a gap |
| **Audience** | Words the decider would not use are replaced or defined |

Fix what fails, then say what you fixed in one line each.

## 6. Hand over an outline

Give a Markdown outline any slide tool can build from:

```markdown
## Slide 3 - Two rivals now undercut us on price in our largest segment
- Visual: bar chart, our price vs two rivals, last 4 quarters
- Proof: rival A 12% lower since Q2; rival B 9% lower since Q3
- Source: public price lists, checked 1 Mar
- Speaker note: we lost 3 renewals citing price
```

Then offer to build the slides with whatever slide tool is available. **Do not design before the
user has seen the headlines.** Changing a headline costs a minute now and an hour after design.

## Limits, said plainly

- **This builds the argument, not the visuals.** It needs a slide tool or skill for those
- **It cannot check facts it was not given.** It marks them as gaps and never fills them

Sources and design notes: [references/sources.md](references/sources.md).
