# Where this design comes from

The Gauntlet Loop is Matt Shumer's method. This skill is an independent, cost-capped adaptation of
it, written from the sources below, which were read on 31 Oct 2026. The links were rechecked on
1 Nov 2026. Findings are as those sources report them.

## The method

- **[How to Run a Gauntlet Loop](https://somethingbig.ai/gauntlet-loop), Matt Shumer.** The origin:
  a goal and a concrete bar, small separately judged pieces, a fresh critic for each piece, and a
  loop until the bar is met. Shumer advises against a fixed round count, and this skill departs from
  that on purpose. Where cost matters a cap is the point, and the ratchet means an early stop still
  leaves the best version found
- **[Claude of Duty](https://github.com/mshumer/Claude-of-Duty).** The worked example. Parallel
  rounds did less than one sequential pass with a single owner per coupled concern, and one round
  scored worse than the one before it. That is why coupled pieces run in order, and why the best
  version is kept and the latest is not

## What others found

- **[The Gauntlet Loop, tested](https://wotai.co/blog/gauntlet-loop-playbook).** Four test runs.
  Existing work with a reference converged best, and failures clustered on builds with no anchor.
  That is the basis of the fit check
- **[gauntletx](https://github.com/NathanMaine/gauntletx), Nathan Maine.** Vague bars fail and a
  checkable target works. Local models built acceptably and judged poorly, so they never judge here
- **[gauntlet-loop-cheap](https://github.com/danielsapps2/gauntlet-loop-cheap).** Tiered models
  and agent limits. Its results are self-reported from one run, and the repo shows no licence, so
  this skill cites its idea and uses none of its text
- **[The New Gauntlet Loop Has A Flaw](https://daily.dev/posts/the-new-gauntlet-loop-has-a-flaw-this-claude-skill-just-fixed-it-2u5yvngy5).**
  Novel work has no ready reference, so the critic invents its own standard. Hence the option of an
  answer key, agreed at the gate before any build

## Formats

- **[Agent Skills specification](https://agentskills.io/specification).** The `SKILL.md` format
- **[Claude Code plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces).** How
  this repo is packaged

## One pilot, by the author of this skill

The method was run by hand on three generated reports in Oct 2026, before this skill was written.
These are estimates from token counts at API prices, from one run on one kind of document.

- **Total:** about $15, against a $20 cap
- **Lead session:** the largest single cost, at about a third of the total
- **Haiku on fixed edits:** almost nothing, and it did the job
- **Opus as a builder:** over three times Sonnet's cost for the same result
- **Opus as a final critic:** found four blocking faults after every script and earlier critic had
  passed
- **Faulty captures:** one misled a critic and voided a round, so the capture tool is now proved first
