---
name: capability-ladder
description: Use when a task cannot be done with what is installed, when asked whether a skill, tool, connector or plugin is missing, or for a periodic review of whether the agent's tools cover the standing work. Checks what already exists first, picks the cheapest rung that closes the gap (reuse, compose, script, then third party), and puts a proposal to the user instead of installing anything.
license: MIT
compatibility: Works with any agent. Listing installed skills, tools and connectors depends on what the agent harness exposes.
---

# capability-ladder: reuse before build, build before buy, and every install is a proposal

**A capability gap is not permission to install.** Installing a plugin or authorising a
connector grants authority, and authority is asked for, never assumed. The agent prepares; the
user approves.

The failure this prevents is cheap and common: **a capability rebuilt because nobody looked.**

**Read the project's own rules, then the personal overlay at
`~/.config/skillknot/capability-ladder.md` if it exists.** It may list where scripts, skills and
scheduled jobs live, and where decisions are recorded.

## 1. Check what is already there

Check every place before calling anything missing:

| Place | How to look |
|---|---|
| **Project scripts** | The script index or README. Search by what a script does, not what you would have named it |
| **Skills** | The installed skill list, and the project's own skills folder |
| **Connected tools and connectors** | The tool list now, then any registry of connectors that exist but are not connected |
| **Agent types** | The available subagents. A specialist is often the answer |
| **Scheduled jobs** | The scheduler's list, and the project's job definitions |

## 2. Name the kind of gap

| Kind | Answer |
|---|---|
| **It exists and you did not know** | Use it. Not a gap: a lookup miss, worth one line in the report |
| **It exists but is not connected** | An authorisation proposal. The user's click, not yours |
| **It can be composed from what is here** | Compose it. A script plus a skill is not a purchase |
| **It needs new code** | A script proposal: the cheapest real addition, and it stays in the project |
| **It needs a third party** | A connector or plugin proposal: the most expensive, and the only one with an ongoing trust cost |

**Prefer the cheapest rung that actually closes the gap.** A connector installed to do what a
twenty-line script would do is a permanent dependency bought for a one-off.

## 3. Put the proposal

```markdown
**Gap:** what could not be done.
**Exposed by:** the real task that hit it, with a link. Never hypothetical.
**Checked:** each place in step 1, and what was found.
**Candidate:** the skill, connector, agent or script, by name.
**Cost:** the user's time, a permission, a dependency, an ongoing token or money cost.
**Alternative:** the runner-up and what it gives up. One only.
**Recommendation:** the pick, with confidence: confident, fairly sure or guessing.
```

- **Never hypothetical.** A gap with no task behind it is a shopping list. A periodic review is
  allowed, and it still names the standing work that is not covered
- **Installing, authorising and paying are the user's actions.** You may prepare the config,
  write the script or draft the settings change

## 4. Record the outcome

- **Record every decision:** installed, authorised or declined, **with what was rejected and
  why.** A declined proposal left unrecorded comes back next quarter with nothing new
- **A new script gets a header:** what it does, how to run it, and what it writes

## 5. Periodic review

Run it when the shape of the work changes, not on a clock:

1. List the standing work: live projects, recurring routines, scheduled jobs
2. For each, name the capability it relies on and where it sits
3. **Anything that relies on someone remembering to do it by hand is the gap**
4. **Anything running unattended must report somewhere visible.** A job that reports nothing
   cannot be told apart from one that never ran

Sources: [references/sources.md](references/sources.md).
