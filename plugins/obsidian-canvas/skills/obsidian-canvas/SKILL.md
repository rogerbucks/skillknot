---
name: obsidian-canvas
description: Use when asked for an Obsidian canvas, a map or visual diagram of notes, "show how these connect", or when a topic's structure would read better drawn than written; also to check, repair or extend an existing .canvas file. Builds JSON Canvas files from real note links joined by labelled edges, lays them out to read on desktop and mobile, and verifies them before writing. Not for Mermaid inside a note, HTML canvas, Canva or a learning platform.
license: MIT
compatibility: Works with any agent that can read and write files in an Obsidian vault. Graphviz (dot) is optional, for placing larger graphs. No Obsidian plugin is required.
---

# obsidian-canvas: draw the graph, then prove it reads

**A canvas that renders is not a canvas that reads.** Every rule below serves that difference.

**Read the vault's own rules, then the personal overlay at
`~/.config/skillknot/obsidian-canvas.md` if it exists.** It may name a colour scheme, an icon
vocabulary, folders and node sizes.

## The rule

> **Build a canvas from `file` nodes that point at real notes, joined by labelled edges, and
> verify it before writing it. Use text nodes for headings and notes, not for content that
> already has a note.**

A canvas full of text boxes is a picture beside the vault: invisible to search, backlinks and
the graph view. File nodes keep it part of the vault.

## Once the user arranges it, the canvas is the source

**Layout is Obsidian's job.** Its edge router is not documented, so no generator can predict how
it will draw connectors, and a layout that "checks clean" can still read badly. A person
dragging one node settles it for good.

- **Generate a canvas once,** as a first draft
- **After the user has arranged it, never regenerate positions.** Edit it in place: add or
  change nodes and edges, and keep every existing `x`, `y`, `width` and `height`
- **Regenerating an existing canvas destroys the arrangement.** Say what would be lost and let
  the user decide

## Procedure

### 1. Decide the graph before any geometry

Nodes and edges first, positions later. If the structure is not yet decided, that is thinking
work: do it in prose or a Mermaid sketch first. **This skill draws a decided structure. It does
not invent one.**

For each node, ask whether a note exists:

| Answer | Node |
|---|---|
| Yes | `file` node, with the path relative to the vault root |
| No, but it should | `text` node: a `## Name` heading, a one-line description, then `[[Name]]`, so a click creates the note |
| No, it is a label or grouping | `text` node, or a `group` with a `label` |

**Never point a `file` node at a note that does not exist.** It renders as an empty box with no
error anywhere.

### 2. Label every edge

An unlabelled edge says only "these are related", which nearness already says. Use lowercase
verbs read in the direction of the arrow: *shapes*, *is the source of*, *blocks*. Labelled edges
make a canvas read as an argument, not a cloud.

### 3. Lay it out

- **Put linked nodes next to each other.** Column order decides how many edges span far
- **Size the gaps for the edge labels.** Obsidian draws a label at the middle of its connector,
  so a small gap hides the label behind the nodes. About **180 px across and 150 px down**
  clears a typical label
- **At most three nodes a row, then wrap,** and **about four columns at most.** Prefer depth to
  breadth: a phone scrolls down easily and pans sideways badly
- **An edge between two wrapped groups leaves from the group's last row,** or it cuts through
  the rows below
- **A card with a long title needs height, not only width.** About 120 px
- **Colours `1` to `6` only,** matching any scheme the vault already uses

**For more than a handful of nodes, let Graphviz place them** (`dot -Tjson`). Use it for
positions only, because Obsidian draws its own connectors and ignores supplied paths. Two traps:
Graphviz gives node **centres** in points with sizes in inches (72 points to the inch), and **its
Y axis runs upwards**, so flip Y against the bounding box. JSON Canvas needs **whole-number
coordinates**, so round every value.

### 4. Route long edges clear of nodes

- **An edge spanning several rows in one column** leaves from the left side, runs down a lane
  clear of the column, and comes back in from the left
- **A feedback edge** leaves from the right, rises above the rows it joins, and drops in from
  the top
- **Headings sit above any feedback lane**

### 5. Verify before writing

Check these, by reading the JSON:

| Check | Why |
|---|---|
| **No edge passes through a node it does not join** | A crossing count misses this, and it makes a fan-out look like a chain |
| **Every `file` node points at an existing file** | A missing target fails silently |
| **Coordinates are whole numbers and ids are unique** | Required by the JSON Canvas format |
| **Colours are from the vault's set** | Report drift. Do not fail it |
| **The file is written the way Obsidian writes it:** tab-indented, with any object or list that holds only plain values kept on one line | Otherwise Obsidian rewrites the whole file on first open, and the next real diff is noise |

The "passes through" check is an estimate of Obsidian's routing. A hit is strong evidence, and a
miss is not proof, so **look at the rendered canvas** too.

## What a canvas can hold

| Want | Node |
|---|---|
| A note, or one section of it | `file`, plus `subpath: "#Heading"` for a section |
| An image or diagram | `file` pointing at an `.svg` (sharp at any zoom, and searchable) or `.png` |
| A web page | `link` with a `url` |
| A flow inside the map | `text` with a fenced Mermaid block. It renders natively, also on mobile. Keep it small |
| A titled region | `group` with a `label`, and optionally a `background` image |

**Never depend on a plugin for legibility.** Custom shapes and canvas plugins are often missing
on mobile, and CSS shapes change how a node looks, not its geometry. Leave extra clearance
around shaped nodes.

## Known traps

- **A `file` node is a path, so it breaks when a folder is renamed.** After any folder rename,
  check every canvas that points into it
- **Do not retrofit old canvases in bulk.** It is a destructive edit across many files for no
  stated need. Ask first

## Finish the job

- Put the canvas **in the folder of the topic it concerns**
- **Link it from that topic's index note,** or it can only be found by browsing
- **A canvas earns its place when the shape is the point:** a chain, a fan-out, a cycle. Under
  about three nodes, it is ceremony

Sources: [references/sources.md](references/sources.md).
