# Where this design comes from

Written fresh for this repo. No text was copied from the sources below, which are widely used
planning practices.

- **Project charters and one-page plans.** A goal, the people it serves, the limits and the next
  actions, kept short enough to read at a glance
- **Open-issues logs.** A visible list of what is undecided, so questions get answered instead of
  forgotten
- **Next actions.** Each step is a concrete thing someone can do, starting with a verb

## Design choices

- **Five fields, no more,** so the pane fits beside the chat and reads in seconds
- **The agent fills it, not a scan of the chat.** A mod cannot judge what a plan is; the agent
  can, and it already knows when the plan changed
- **Lists are replaced whole,** so a stale item never lingers after the agent rewrote the list
- **A plan block in the chat when there is no pane,** so the skill works with any agent
- **The pane opens itself only when planning starts,** so it stays out of the way otherwise
