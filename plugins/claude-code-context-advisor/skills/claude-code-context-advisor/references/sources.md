# Where this design comes from

Written fresh for this repo. No code was copied. The links were read on 1 Nov 2026.

- **[Claude Code hooks](https://code.claude.com/docs/en/hooks).** Each hook is given a
  `transcript_path`, the session record this script reads
- **[Claude Code status line](https://code.claude.com/docs/en/statusline).** How Claude Code
  counts context in use: input tokens plus cache reads and cache writes from the latest reply.
  The script uses the same sum
- **Session records.** One JSON object per line, with tool calls, their results and each reply's
  token counts. The fields read are `message.content`, `message.usage`, `isSidechain` and the
  compaction markers. They were checked against a current record on 1 Nov 2026

## Design choices

- **Advise, never act.** Compacting or clearing loses detail, so the user decides
- **Count only since the last compaction,** because earlier reads are no longer in context
- **Sizes and names, never contents,** so the report can be read safely
- **A few clear thresholds,** not a score. Each finding says what to do differently next time
- **Separate from `context-budget`,** which measures what is loaded before a session starts. This
  looks at what a session did once it was running
