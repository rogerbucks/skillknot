---
name: document-bundle
description: Use when one document needs other versions (HTML, Word, slides, a one-page summary, a version for a specific audience), when asked to publish something for a person or group, when a derived copy may be stale, or when asked what versions of a document exist. Keeps one canonical source, derives every version from it, records the set, checks freshness, and never sends anything.
license: MIT
compatibility: Works with any agent that can read and write files. Making Office files needs a converter such as pandoc or a document library; Markdown and HTML need nothing extra.
---

# document-bundle: one source, every version derived from it

**A bundle is one canonical source file, every version derived from it, and the small side files
they depend on** (an audience list, a style file, a reference list). **Only the source and the
side files are ever edited by hand.** If you are editing a derived version, stop: you have just
made a second source, and the two will drift.

**Read the project's own rules, then the personal overlay at
`~/.config/skillknot/document-bundle.md` if it exists.** It may name where the registry lives,
the audiences, a house style and the converter to use.

## Which job is this?

| Ask | Do |
|---|---|
| "Make this a proper document", "give it an HTML version" | **Register:** section 1 |
| "Send this to the board", "publish it for the team" | **Publish:** section 2 |
| "Is this current?" | **Check:** section 3 |
| "What versions exist?" | **Inspect:** section 4 |

**Bundle a document when nobody will read it whole** (about ten sections or more), or when
someone other than its author will read it. Below that, a document is just a document.

## 1. Register

1. **Record the bundle** in one registry file: the source path, each derived path, the audiences,
   and the side files. Derived paths follow the source's name, so the set is easy to find
2. **Mark the source** with a short note at the top naming it as the source, so nobody edits a
   copy by mistake
3. **Generate the first derived versions,** then **look at the rendered result, not the markup.**
   Rendering defects rarely show in source

## 2. Publish to an audience

- **If the audience is not named, ask.** Name the two or three that fit this document, what each
  would receive, and recommend one. Never present the whole list as a menu
- **Select, then rewrite.** Choosing the sections an audience needs is mechanical. Rewriting the
  prose in that audience's register is judgement, and **skipping it is how a document reaches an
  executive in a delivery team's voice**
- **Respect sensitivity.** If something was withheld for this audience, **say so in chat as well
  as in the file,** so the author sees it before sending
- **Format follows the content:** Markdown or HTML for reading, a Word file for mark-up, a
  spreadsheet for tables, slides for a briefing
- **Office files are outputs, never sources.** If someone marks up a Word copy, carry their
  changes back into the source by hand, then regenerate
- **Never send it.** Publishing writes files. Delivery is the author's

## 3. Check freshness

A derived version is stale when the source or a side file changed after it was made. **Say which
one changed,** because the fix differs: a source change means regenerate, and a side-file change
may mean the audience or style is now wrong.

## 4. Inspect

List the source, each derived version with its date, the audiences, and anything stale.

## Reshape

- **Split** a bundle when one part has its own audience and its own rate of change
- **Merge** two when they keep repeating the same table or section
- **Repeated content is a sign of a missing shared side file.** Move it there once, and derive it

Sources: [references/sources.md](references/sources.md).
