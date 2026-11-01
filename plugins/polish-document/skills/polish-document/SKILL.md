---
name: polish-document
description: Use when asked to review, tidy, professionalise, reformat or restructure a document, when notes are rough or raw, or when a capture needs to become a real document. Runs five passes in order (missing sections first, then review, Markdown format, diagrams, and a hand-off) and keeps the author's words separate from proposed additions.
license: MIT
compatibility: Works with any agent that can read and write Markdown files. Diagrams use Mermaid, which needs a renderer that supports it.
---

# polish-document: a rough capture becomes a professional document

**The failure this prevents:** a document gets tidied, and the tidying is the whole change.
Typos fixed, bullets aligned, and nobody asks what the document is missing. **Formatting is the
cheapest pass and the least valuable.**

**Before pass 1, read the project's own rules, then the personal overlay at
`~/.config/skillknot/polish-document.md` if it exists.** It may set a house style, frontmatter
fields, folders and a voice.

**Five passes, always in this order.** Structure before prose, prose before format, format before
pictures. Each pass is wasted if a later one moves the furniture.

| Pass | Question | Output |
| --- | --- | --- |
| **1 Gaps** | What should be here and is not? | A ranked list of missing sections |
| **2 Review** | What reads as unfinished? | Fixes, and a short list to raise |
| **3 Format** | Does it meet standard Markdown? | The rewritten document |
| **4 Diagrams** | What is the prose carrying badly? | Mermaid, in the document |
| **5 Hand off** | Does it need more than one version? | A pointer to the right tool |

**Read the whole file before proposing anything.** Never polish from an excerpt.

## Pass 1: gaps

**This pass holds the value, so do it first,** while the original shape is still visible. Once
formatted, a document looks finished and its gaps stop being obvious.

- **Read for what the document is for, then ask what a competent version contains.** A strategy
  without decision rights. A runbook without a rollback. A plan without a stop condition
- **Walk any chain.** Where the document cascades (direction, plan, budget, delivery), name the
  link that is asserted but not built
- **Name each gap in one line: what is missing, and what breaks without it.** A gap without a
  consequence is a suggestion, and gets ignored
- **Never slip invented content into the author's text.** Put proposed sections at the end, in a
  clearly marked block:

  ```markdown
  > [!note]- Proposed additions, not yet adopted
  >
  > Gaps found on <date>. Promote any that earn their place, and delete the rest.
  ```

  **The author's words and yours must stay separable.** The author promotes them, not you.

## Pass 2: review

Fix without itemising:

- Typos, broken sentences, stray fragments, empty bullets, duplicate lines
- Mixed bullet markers, mixed tabs and spaces, orphan indent levels
- **Bold used as a heading:** a bold line on its own is a heading, so make it one
- A voice that switches person part way through

Raise, do not fix:

- **A title that is a date, not a subject.** Rename it to what it is about
- **Claims that could embarrass the author in front of the reader:** an unsupported number, a
  named company, a figure from a secondary source. Mark it as unverified rather than deleting it
- **Anything that reads as a decision or an action.** It belongs in a decision record or a task,
  not buried in prose

## Pass 3: format to standard Markdown

- **One `#` title.** `##` for sections, `###` below that. Never bold in their place
- **`-` for bullets.** Numbers only where the order is real
- **A table wherever items are compared on the same points.** A bullet list of parallel items is
  a table that has not been written yet
- **A blank line around every heading, table, list and code block**
- **Bold the phrase that carries the weight,** not the whole sentence
- **Concise and direct.** It will be reread by someone who knows the context and has little time

## Pass 4: diagrams

**Draw one only where structure is the point.** A diagram that repeats the sentence above it is
worse than none. Use Mermaid in the document, so it stays searchable and diffable.

| Shape in the document | Diagram |
| --- | --- |
| A cascade or layers | `flowchart TD`, with any feedback edge dotted |
| A loop: plan, do, check, decide | `flowchart LR` with a decision node |
| A lifecycle with a stop condition | `flowchart TD`, the failure path dotted |
| Two options being weighed | One diagram each, side by side |

**Keep them plain.** No colour classes or styling, and nest groups at most one deep, so the
diagram suits light and dark themes. **In a chat reply, use a table or ASCII instead,** because
most chat surfaces do not render Mermaid.

## Pass 5: hand off

If the document is long enough that nobody will read it whole (about ten sections or more), or
several audiences will read it, it needs a single source with derived versions. **That is the
`document-bundle` skill's job.** Say so and stop.

## Where the result goes

**Never overwrite the original in place,** unless the user asks. Then take a backup first.

- **Write the polished version as a new file** beside it, or where the project files such
  documents
- **Mark the original as superseded,** with a link forward. Do not delete it without the user's
  say-so
- **Say plainly that two copies now exist,** and recommend which to retire

## Report

Bottom line first, then:

- **The gaps, ranked.** This is the value, so it leads
- **What was fixed,** in a sentence
- **What needs the user's decision:** the title, the two copies, anything raised in pass 2
- **A link to the new file**

Sources: [references/sources.md](references/sources.md).
