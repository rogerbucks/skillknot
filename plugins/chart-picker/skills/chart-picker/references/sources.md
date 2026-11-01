# Where this design comes from

Written fresh for this repo. No text was copied from the sources below, which are well-known
work in data visualisation and accessibility.

- **Graphical perception research.** People judge position and length more accurately than
  angle, area or colour. Associated with Cleveland and McGill's studies of the 1980s
- **Data-ink and chart-junk.** Remove what does not carry data. Associated with Edward Tufte
- **Accessibility guidance.** The Web Content Accessibility Guidelines say colour must not be the
  only way to convey meaning, and that images need text alternatives
- **Colour vision deficiency.** Red-green colour blindness affects about 1 in 12 men and 1 in 200
  women of northern European descent, per widely cited estimates

## Design choices

- **Start from the reader's question,** because the same data needs different charts for
  different questions
- **A short "avoid" column,** because the common mistakes (pies, dual axes, truncated bars) cause
  most misreadings
- **The headline states the finding,** so the chart is proof, not a puzzle
- **Spec or build, never invent.** Missing data is shown as missing
