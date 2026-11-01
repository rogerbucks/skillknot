# Where this design comes from

These were written fresh for this repo from a method developed and used in one person's private agent setup. No text was copied from that setup or from the sources below, which were read on 1 Nov 2026.

- **[JSON Canvas 1.0 spec](https://jsoncanvas.org/spec/1.0/).** Node types, edges, groups and
  integer coordinates
- **[Graphviz JSON output](https://graphviz.org/docs/outputs/json/).** Positions for larger
  graphs, and the Y-axis flip
- **Private use.** The layout gaps, the "edge through a node" check, the mobile width cap and the
  rule that an arranged canvas is never regenerated all came from canvases that rendered but read
  badly
