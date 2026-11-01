---
name: ownership-map
description: Use when asked who owns or controls a company, who is behind it, what else its owners hold, how a sector is carved up, whether two companies are connected, or where a conflict of interest sits. Climbs to the ultimate controller, maps sister assets, compares each entity's stated purpose with where its money goes, and separates aligned interest from proven coordination.
license: MIT
compatibility: Needs web search. Works with any agent. Drawing the map needs a surface that renders diagrams; otherwise it falls back to Mermaid or a table.
---

# ownership-map: who actually benefits, and from what?

A company's registered owner is rarely the interesting answer. The interesting answer is the
**ultimate controller**, the **sister assets** that share that controller, and the **gap between
what the group says it is for and what its money does**.

**Read the project's own rules, then the personal overlay at
`~/.config/skillknot/ownership-map.md` if it exists.** It may say where maps are filed and which
sources to prefer.

## Five passes, in order

Each pass has a stopping point. Go no deeper than the question needs.

### 1. Climb to ultimate control

Follow the chain until you reach **a person, a family trust, a state fund, or a genuinely spread
public register.** Stop there, and say which of the four you reached.

- **Control is not ownership.** Look for dual-class shares, voting caps, trusts and shareholder
  agreements. A 20% voting stake with board seats beats a 30% economic stake without them
- **Name the instrument.** "Class B voting shares held by a trust" is an answer. A family name is
  not
- **A minority holder moving towards control is a finding.** Note anyone above about 15% with a
  stated or reported intent

### 2. Fan out to sister assets

From the controller, list **every material asset,** not only those in the same sector. The
cross-sector holdings are usually where the conflict sits.

- Include **private vehicles the controller holds personally.** They appear in no listed filing
  and are the piece most often missed
- Include **minority stakes above about 5%,** marked as minority
- Include **assets sold in the last two years,** marked as historic. A recent exit still explains
  behaviour

### 3. Stated purpose against behaviour

**This pass makes the map worth reading.** For each significant entity:

| Column | Source | Test |
|---|---|---|
| **Stated purpose** | Annual report, "about us", investor day, chair's letter | Quote or paraphrase closely. Do not editorialise |
| **Behavioural motive** | Where revenue and capital actually go | What would this entity fight hardest to protect? |
| **The tell** | One observable, citable fact | Would a sceptic accept this one fact as evidence? |

**Every behavioural claim needs a tell.** Without one it is an opinion: label it or drop it. The
tell is usually a number (revenue share, capital spend), a transaction, or a public position
taken against apparent self-interest.

### 4. Constraints

What could change the picture:

- **Live regulatory action:** investigations, notices, court cases, inquiries
- **Real competition:** who is funded to attack, and how
- **Law that does and does not reach it.** Naming the gap is often the sharpest finding

### 5. Where interests align

**Alignment is not collusion, and the difference is not optional.**

- **Say "aligned interest" and show the mechanism:** the same revenue exposure, the same lobbying
  position, the same regulatory threat
- **Never assert coordination** without documented evidence of it
- **Note where the same parties compete.** It is the honest counterweight, and it makes the
  alignment findings credible

## Output

**Three or more entities: draw it.** Cards cannot be compared, and a table flattens
containment, which is the whole subject here.

- **The company is the box; its controller is a fact inside it.** Drawn the other way, the map
  reads as an org chart of owners, not a map of the sector. Group by controller when the question
  really is "who holds what"
- **Side by side means "compare these". Stacked means "and also".** Place things side by side only
  when they are values of the same measure. Two different facts about one entity stack, or the
  layout claims a comparison the data does not support
- **Never lump unlike owners into one residual box** such as "others" by default. Model each one,
  and offer a roll-up only as an option
- **Colour by one question at a time,** such as exposure to a regulator. A parent box takes the
  strongest value its children hold
- **Where interactive diagrams are not available,** use a Mermaid chain, top down: controller,
  holding company, operating entities, brands, with each edge labelled by percentage and
  instrument. In chat, where Mermaid often does not render, use a table or ASCII

**Every claim group carries a confidence band:** confident, fairly sure, or guessing. Mark
figures from trade press or other secondary sources as unverified.

## What this skill will not do

- **Assert collusion.** Alignment, yes, with the mechanism. Coordination, only with evidence
- **Infer editorial direction from ownership.** That is a separate claim needing its own proof
- **Treat estimates as audited.** Market shares quoted by participants are claims
- **Map private individuals.** Executives and controlling shareholders in their corporate role,
  yes. Private people, no

## Speed

Six to ten searches cover most subjects. Run them in parallel batches: the ownership chain, the
sister assets, the controlling person or trust, live regulatory action, the main competitor and
its owner, and the stated strategy. **Do not read whole annual reports.** The stated purpose is
in the first two pages, and the motive is in the segment revenue table.

Sources: [references/sources.md](references/sources.md).
