# Where this design comes from

These were written fresh for this repo from a method developed and used in one person's private agent setup. No text was copied from that setup or from the sources below, which were read on 1 Nov 2026.

- **[Claude Code memory and instruction files](https://code.claude.com/docs/en/memory).** What
  loads on every turn
- **Private use.** Always-loaded instructions grew by a section per decision, an index drifted
  to omit most of its rules, and a slow per-turn hook went unnoticed. Measuring each, with a
  budget, made the drift visible. Relocating rather than deleting kept every fact
