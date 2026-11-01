---
name: chart-picker
description: Use when the user wants to show numbers or data visually, asks which chart to use, or wants a chart, graph, dashboard tile or table reviewed or made clearer. Picks the chart from the question the reader is asking, keeps axes and scales honest, writes a headline that states the finding, and makes it readable by colour-blind readers and in black and white.
license: MIT
compatibility: Works with any agent. Gives advice and chart specifications. Drawing the chart needs a charting tool, spreadsheet or code, which this does not supply.
---

# chart-picker: the chart that answers the question

**A chart answers one question.** Start from the question the reader is asking, not from the
shape of the data or the tool's default. The wrong chart type is the most common reason a true
number gets misread.

**Read the personal overlay at `~/.config/skillknot/chart-picker.md` if it exists.** It may set
brand colours, fonts, a charting tool or house rules.

```text
1 Question -> 2 Pick -> 3 Make it honest -> 4 Make it readable -> 5 Headline -> 6 Check
```

## 1. Name the reader's question

Write it as a sentence: *"Is churn getting better or worse?"* If there are two questions, there
are two charts.

## 2. Pick from the question

| The reader asks | Use | Avoid |
| --- | --- | --- |
| **How has it changed over time?** | Line chart. Columns if there are fewer than about 8 periods | Pie, area stacks of many series |
| **Which is biggest, and by how much?** | Horizontal bars, sorted largest first | Pie with more than 3 slices, 3D anything |
| **What share is each part of the whole?** | One stacked bar, or a pie with 2 or 3 slices | Pie with many slices, donut with a number hidden in the middle |
| **How does a part change its share over time?** | Stacked columns as 100%, or small multiples | Stacked area with more than 4 series |
| **Are two measures related?** | Scatter plot, with a trend line only if it is meaningful | Two lines on two different axes |
| **How is it spread out?** | Histogram or box plot | An average on its own |
| **Where is it?** | Map, only if place is the point | A map when a sorted bar would do |
| **Did we hit target?** | Bar or bullet chart with the target marked | Gauges and dials |
| **What exactly is the number?** | A table, or one big number with its comparison | A chart that makes the reader guess values |

**When in doubt, use a sorted bar chart or a line chart.** Readers judge length and position far
more accurately than angle, area or colour.

## 3. Make it honest

- **Bars start at zero.** A bar's length is its value. Lines may zoom in, if the axis says so
- **Same scale across charts that will be compared,** or say clearly that they differ
- **No second y-axis.** Two axes let any two lines look related. Use two charts side by side
- **Show the time period and the unit** on every chart
- **Do not cherry-pick the window.** If a longer view tells a different story, show it or say so
- **Mark gaps, estimates and forecasts** differently from actuals, such as a dashed line
- **Percentages need their base.** "Up 50%" from 2 to 3 is not news

## 4. Make it readable by everyone

- **Never use colour as the only signal.** Add labels, patterns or position as well. About 1 in
  12 men cannot tell red from green
- **Use a colour-blind-safe palette,** such as one built for it, or shades of a single hue
- **One highlight colour** for the thing the headline is about. Grey for everything else
- **Label lines and bars directly** instead of using a legend the eye must cross back and forth
- **Text at a readable size,** horizontal, with no rotated labels. Flip to horizontal bars if
  category names are long
- **Check it in black and white.** If it still reads, it is robust
- **Give alt text** that states the finding, not the chart type: "Churn fell from 6% to 4% over
  2025"

## 5. Write the headline as the finding

| Title (avoid) | Headline (use) |
| --- | --- |
| Monthly churn 2025 | Churn fell by a third in 2025, mostly after the March price change |

The headline says what to see. The chart proves it. Remove anything that does not help prove it:
gridlines, borders, shadows, decimal places nobody needs.

## 6. Check before handing over

| Check | Pass when |
| --- | --- |
| **Five-second test** | Someone new can say the finding within five seconds |
| **Honest axes** | Bars start at zero, scales match where compared, the unit and period are shown |
| **Source** | The source and date sit under the chart |
| **Accessible** | Works without colour, and has alt text |
| **No invention** | Every value came from the data given. Missing data is shown as missing |

Hand over the spec (chart type, data, highlight, headline, notes) or build it with the tool the
user has. Say which checks it passed.

Sources and design notes: [references/sources.md](references/sources.md).
