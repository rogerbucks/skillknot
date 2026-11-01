# Handover

Where SkillKnot stands, and what comes next. Date: 1 Nov 2026. Follow [AGENTS.md](../AGENTS.md)
throughout. This file holds the reasoning that the code cannot.

## What is live on `main`

**20 plugins, one skill each.** The README lists them all. In groups:

- **Improve and review:** `gauntlet` (builder and critic rounds against a bar), `adversarial-review`
  (a hostile expert panel by region, phase and industry), `private-words` (keeps private words out
  of a repo)
- **Sessions and documents:** `handoff`, `polish-document`, `document-bundle`, `verdict-first`
- **Presentation and design:** `slide-storyline` (one headline claim per slide), `chart-picker`
  (the chart from the reader's question, honest and colour-blind safe), `design-brief` (a one-page
  brief agreed before building)
- **Research and risk:** `ownership-map`, `read-only-researcher`, `taxonomy-review`,
  `threat-model` (what could go wrong, cheapest fixes first, report only)
- **Running an agent setup:** `capability-ladder`, `context-budget`, `model-picker` (the cheapest
  model tier that does each step well)
- **Claude Code hooks:** `claude-code-guards` asks before pushes, destructive commands and
  connector sends, refuses secret paths, and warns when a web or connector result tries to give the
  agent orders. `claude-code-session-meter` adds a status line, a cost, time and prompt cap, and a
  handoff reminder
- **One app:** `obsidian-canvas`
- **The gate:** pull requests only, rebase merges only, and `checks`, `lint` and `review` must
  pass. Links are checked locally, not in CI: `python3 scripts/links.py`
- **Automatic review and merge:** `review.yml` has an automated reviewer read each pull request
  against AGENTS.md, post one comment, and fail on a BLOCK verdict. `auto-merge.yml` turns on
  rebase auto-merge for the owner's own non-draft pull requests. A merge made by the workflow token
  does not start the `push` run of CI on `main`, so `main` is checked only through its pull
  requests. A pull request that changes `review.yml` cannot pass `review`, so the owner merges it
  by hand

## Do this first

**Give the newest items a live run.** Everything added on 1 Nov 2026 passed its tests and an
automated review, but none has run in a real session yet.

1. **Install the two hook plugins** in a scratch project and try each guard: `git push`,
   `git reset --hard`, reading `~/.ssh/config`, and a web page that quotes "ignore previous
   instructions". Each should ask, refuse or warn as its skill says
2. **Set up the status line** by hand, as the `claude-code-session-meter` skill describes. A
   plugin cannot set it. Check that the cost and context figures match Claude Code's own
3. **Run each new skill as a stranger:** `slide-storyline`, `chart-picker`, `design-brief`,
   `threat-model` and `model-picker`. Paper runs earn their keep: the one for `private-words`
   found a word leaking through a printed file name
4. **Known small gaps,** left on purpose: the tripwire can flag an ordinary line that starts with
   "System:", and the handoff reminder treats any skill call that mentions "handoff" as a handoff

## How to ship a change here

- **One branch per pull request, made from `main`.** Reusing a merged branch needs a force push,
  which the agent's safety check refuses. A fresh branch name avoids that
- **Keep hooks apart from skills.** Hooks can stop or steer an agent, so they get their own pull
  request and their own review
- **Open as a draft, then mark it ready once checks pass.** Marking ready starts a second review.
  The reviewer's nits are optional; carry the good ones into the next pull request

## `adversarial-review`: what to know

- **Sources are links, not copies.** Each standard has an ID, its official link, a short cached
  note and the date the link was last confirmed. About 95 rows across global, US, EU, UK,
  Australia and New Zealand, Asia Pacific and Canada were opened on 1 Nov 2026
- **Rows marked *never*** could not be confirmed that day: the page refused automated reads or
  rendered empty. The skill refreshes them on first use. Check them by hand when convenient:
  `GL-ISO42001`, `GL-UNGP`, `US-COAI`, `EU-NIS2`, `EU-GREEN`, `EU-CSRD`, `AU-E8`, `IN-DPDP`,
  `HK-PDPO`, `CA-QC25`
- **Weekly freshness, at run time.** Any standard in use that was checked more than 7 days ago is
  reopened and written to a local cache outside the repo. A scheduled link checker was tried and
  dropped by the owner: government sites block it, so about 38 of 157 links fail falsely. The
  `links` CI job was removed for the same reason. `scripts/links.py` runs by hand and only fails
  on a 404, 410 or missing host
- **Lifecycle and industry sweep.** `references/lifecycle.md` maps ten company phases (formation
  to exit) and ten industries to the extra audiences, lenses, standards and experts each brings.
  Its last section lists registry gaps it found: employment, insolvency, competition and takeover,
  sanctions and export, safety and environment, child safety and charity codes, professional
  conduct. Fill those one region at a time
- **Not proven:** no live run yet, and no stranger dry-run beyond the author's paper run

## Why it is built this way

- **One plugin per skill,** so a restricted machine can install only what is allowed
- **Fresh general text, never copies.** Each copy would have to be cleaned by eye, and versions
  would drift
- **Personal rules stay outside the repo,** in `~/.config/skillknot/<skill>.md`
- **Limits go in `compatibility`, and model names only in `references/models.md`.** Vendor folders
  would duplicate skills and let them drift
- **CI only reads.** Fix-ups run on the author's machine through `tidy.py`, so nothing pushes to
  `main` by itself
- **Committer names are not checked.** GitHub writes the owner's display name on rebase merges, and
  the owner chose to keep it. Author names, emails and messages are still checked
- **CI checks out the pull request's head commit,** because GitHub's temporary merge commit carries
  the display name and would fail the check

## What to build next

**A context advisor is being built next:** it reads a session's record and says which big files
were read whole when a section would do, what was read twice, when to compact or start fresh, and
when a cheaper model or a subagent would do.

A script should take every step that needs no judgement. These five `gauntlet` scripts are
proposals, and none has been built or run. Savings would be estimates, drawn from one pilot.

- **Plan check:** confirms the plan has all its sections and a machine bar before the gate. It
  stops the costliest failure, a vague bar
- **Blind pair maker:** handles the random order, copying and label stripping, so nothing leaves a
  clue that voids a round
- **Capture proof:** compares a capture against a known page. The pilot lost a round to a bad
  capture
- **Cost tally:** adds up tokens and cost from session records. The lead session was the largest
  cost in the pilot
- **Swap check:** confirms that run-only lines are gone, and that nothing outside the item changed

Keep models for the bar itself, whether a change is better, and clashes between pieces. Adding a
script gives a skill something that can act, so each needs a line in `reviewed-powers.json`.

## Not yet proven

- **`gauntlet` has had no live run** from the published text, and its latest rule and tier edits
  have not been dry-run
- **`private-words` has not been used in a real session.** Its fixes after the paper run are
  covered by tests only
- **The leak check knows only the words on its list.** A clean result says nothing about the rest

## Decisions that stay with the owner

- **Cutting the first release.** No release exists yet
- **Rewriting public history,** which needs a force push
- **Anything pushed to someone else's repo**
