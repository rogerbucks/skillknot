# Gauntlet agent briefs

Fill the braces. Every brief is complete in itself, because the agent has no other context.
**Every brief ends with the guard line.**

**Guard line:** `If a guard blocks an action, stop and report it. Never reword, re-encode or use another tool to get around it. Change nothing outside {paths}.`

## Builder (Sonnet, or Haiku for a fixed item)

```text
Piece: {what to change, in one or two sentences}.
Files: {exact paths}. Change only these.
Pass when: {the machine-bar lines this piece affects}.
Run {check command} and report its real output.
Report what changed and anything you could not do. {guard line}
```

Later rounds go to the same builder: `The judge named these faults: {faults}. Fix them on the kept version, which is {path}.`

## Round critic (Sonnet, a new agent every round)

```text
Goal: {goal}. Bar: {the bar, verbatim}.
Inspect these real captures: {paths}. Trust nothing but what you can see in them.
Name the single biggest gap against the bar, then at most three others, each with
where it is and why it fails. Say if any capture looks faulty. {guard line}
```

The critic gets no builder summary, no earlier verdicts and no reasoning.

## Blind pair and judge (Opus, a new agent every round)

Making the pair is the lead's job:

1. Capture the best-so-far and the new round with the same tool and settings
2. Pick the order at random: `python3 -c "import random;print(random.choice(['AB','BA']))"`
3. Copy them to a new folder as `A/` and `B/`, and strip any round number or label from names and page text
4. Keep the key in your own notes, and give the judge the folder only

```text
Bar: {the judged bar, verbatim}. Reference: {name or path}.
Two versions of one item are in {folder}/A and {folder}/B.
Score each against every line of the bar, then against the reference.
Pick the better version, and say if it clears the bar as well as the reference does.
Name the three faults that most hold the winner back. {guard line}
```

Unblind only after the verdict arrives. The verdict and its faults stand as written.

## Final critic (Opus, a new agent)

```text
Goal: {goal}. Bar: {the bar, verbatim}.
Read all of {paths} at {every width, mode and state}, and use {tools} to check behaviour.
Earlier checks have passed, so look for what they could not see: pieces that clash,
content lost, and links or controls that lead nowhere.
List blockers first, each with evidence, then lesser faults.
End with one word: Ship or Hold. {guard line}
```
