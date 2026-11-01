---
name: taxonomy-review
description: Use when asked to review a folder, category or tag structure, whether there are too many or too few top-level groups, whether one should be split or merged, or where an item should live. Measures size and overlap, recommends merges and splits with an honest confidence for each, and never moves a file without approval.
license: MIT
compatibility: Works with any agent that can list and read the files or records being organised. Needs no scripts.
---

# taxonomy-review: recommend merges and splits, never move a file unasked

**Read the project's own rules, then the personal overlay at
`~/.config/skillknot/taxonomy-review.md` if it exists.** It may say what a top-level group is
called there (theme, area, category), how tags work, and where proposals go.

A **group** is the one place an item lives, such as a folder. A **tag** is a label, and an item
may carry many. The structural question worth asking is whether the groups still carve the
content usefully: **too many tiny groups and nothing can be found; too few huge ones and the
group name says nothing.**

## 1. Measure

For each group, count the items, and note:

- **Size:** the smallest and largest groups stand out first
- **Name overlap:** groups whose names share words
- **Shared tags:** groups whose items carry the same tags
- **Tag clusters inside a large group:** the natural split lines

## 2. Read the signals honestly

| Signal | Means | Confidence |
|---|---|---|
| Merge candidate that **shares tags** | Related content | Reasonable |
| Merge candidate with **name overlap only** | The names look alike | **Weak, and say so** |
| Merge candidate with **neither** | A person must read it | None |
| Split candidate **with tag clusters** | The clusters are the split lines | Reasonable |
| Split candidate with **no tags** | Big, with nothing to split on | None |

**Never present a name-overlap recommendation as if it were based on content.** If few items are
tagged, say that every recommendation rests on size and names alone.

## 3. Propose

One list, each line with the groups, the move, the evidence and the confidence. **Batch the
moves into one approval** rather than asking per item.

## 4. Apply only after a yes

**Moving items between groups is the user's call.** After approval:

1. **Move the item, and leave its tags exactly as they are.** A tag is independent of the group
   that holds it
2. **Fix links that include the old path in the same pass.** Search for them before moving
3. **Refuse on a name clash at the destination.** That is a question of merging or keeping
   separate, never a silent rename
4. **Creating or removing a group needs explicit confirmation,** every time. A tag is not a
   missing group

## Do not

- **Create a group because a tag names one**
- **Duplicate the group name in a tag hierarchy** next to the folder of the same name. Nest tags
  under their own namespace instead
- **Rename an item to get round a clash**
- **Treat a scheduled proposal as approved.** It is a proposal, and a refusal stays on record

Sources: [references/sources.md](references/sources.md).
