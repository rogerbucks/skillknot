---
name: model-picker
description: Use when the user asks which AI model or effort level to use, wants to cut AI spend or speed things up, is setting up subagents, automations or batch jobs, or a task is being run on a bigger model than it needs. Sorts the work into tiers by what it needs, picks the cheapest tier that does it well, tests that choice on a sample, and reports the expected saving.
license: MIT
compatibility: Works with any agent and any vendor. Model names live only in references/models.md. Prices change often, so it reads current prices from the vendor's page or asks; it never relies on remembered prices.
---

# model-picker: the cheapest model that does the job well

**The biggest saving in AI work is not a discount. It is not using the strongest model for
everything.** Most steps in a task are routine. The strongest model is worth paying for only
where judgement is hard and a mistake is costly.

**Read the personal overlay at `~/.config/skillknot/model-picker.md` if it exists.** It may name
the models you can use, your prices, a budget, or rules such as "client data stays on approved
models".

```text
1 List the steps -> 2 Tier each -> 3 Check limits -> 4 Test cheap -> 5 Report the saving
```

## 1. List the steps

Break the job into the steps that actually run: *read 200 emails, sort them, draft replies to 12,
summarise the week.* A single job usually mixes tiers.

## 2. Put each step in a tier

| Tier | Needs | Typical steps |
| --- | --- | --- |
| **Script** (no model) | A fixed rule | Counting, renaming, format checks, finding a word, sorting by date |
| **Fast** | Pattern-following on clear input | Sorting, tagging, extracting fields, short summaries, first drafts from a template, simple lookups |
| **Mid** | Reasoning over moderate context | Most writing and editing, code changes in one area, comparing a few options, answering from documents |
| **Strongest** | Hard judgement, long chains, high cost of error | Architecture and strategy, tricky debugging, legal or financial reasoning, final review of important work, judging other models' output |

Rules for choosing:

- **Start one tier lower than your instinct,** then move up only on evidence from the test
- **Script anything that needs no judgement.** A script is free, instant and never makes things up
- **Use the strongest tier for the bar, not the bulk:** to set the standard, check samples and
  make the final call, while cheaper tiers do the volume
- **Effort or thinking settings are a second dial.** Raise effort before raising the tier for a
  hard but short step. Lower it for routine steps
- **Long, repeated context is a cost in itself.** Reuse cached context where the vendor offers it,
  and send only what the step needs

## 3. Check the limits before the price

Some steps cannot go cheaper whatever the saving:

- **Data rules:** client, health or personal data may be limited to approved models or vendors
- **Context size:** a step that must read a long document needs a model that can hold it
- **Tools:** a step that must use tools, browse or see images needs a model that can
- **Stakes:** if a wrong answer causes harm or cannot be undone, use the stronger tier and keep a
  person in the loop

## 4. Test the cheap choice on a sample

**Never switch a whole job on a guess.**

1. **Pick 5 to 10 real examples,** including at least one hard one
2. **Run the cheaper tier** and the current one on the same examples
3. **Compare against a stated bar,** blind if you can: which output would you ship?
4. **Keep the cheaper tier if it meets the bar.** If it fails only on the hard cases, route just
   those up a tier

## 5. Report the saving honestly

```markdown
**Recommendation:** sorting and tagging on the fast tier; drafting on mid; weekly summary
review on the strongest tier.
**Test:** fast tier matched the bar on 9 of 10 sample emails; the miss was a legal notice,
now routed to mid by keyword.
**Expected saving:** about 70% on this job (~$X a month at today's prices from <vendor page>).
**Risk:** quality drift if email types change; re-test each quarter.
```

- **Read current prices** from the vendor's pricing page, or ask the user. Prices change, so a
  remembered price is a guess
- **Show the arithmetic:** volume times price per tier, before and after
- **Say the confidence** and what would change the answer

## Map tiers to real models

[references/models.md](references/models.md) maps the tiers to each vendor's current models. Add
your own in the overlay. With only one model available, use effort settings and scripts as the
dials instead.

Sources and design notes: [references/sources.md](references/sources.md).
