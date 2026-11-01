# Where this design comes from

This skill is written fresh from general practice in red-teaming, editorial review and compliance
review. It copies no one's text. The standards it lists are linked in [standards/](standards/global.md),
and keep their own licences.

## The method

- **Red teaming and pre-mortems.** A separate team plays the adversary, and a pre-mortem assumes
  the plan has failed and asks why. Both are the root of the hostile reader and `len-premortem`.
  See the [UK Ministry of Defence Red Teaming Handbook, third edition](https://www.gov.uk/government/publications/a-guide-to-red-teaming)
- **Independent reviewers, then cross-examination.** Experts who cannot see each other avoid
  anchoring on the first opinion. A separate check of every quote and clause stops invented
  citations, a known failure of language models
- **Steelman first.** Stating the strongest version of the work before attacking it keeps the
  review on the real item, not a weaker one
- **Graded findings.** Blocker, major, minor and nit follow common code and document review
  practice, so a reader can act on the top of the list and ignore the rest

## Standards and plain language

- **[ISO 24495-1](https://www.iso.org/standard/78907.html)** sets the plain-language bar the style
  lens uses by default
- **Government style manuals** for the US, UK, Australia, New Zealand, Canada and the EU are linked
  in each region's standards file

## Formats

- **[Agent Skills specification](https://agentskills.io/specification).** The `SKILL.md` format
- **[Claude Code plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces).** How
  this repo is packaged
