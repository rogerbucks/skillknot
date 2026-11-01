# Handover

Where SkillKnot stands, and what comes next. Date: 1 Nov 2026. Follow [AGENTS.md](../AGENTS.md)
throughout. This file holds the reasoning that the code cannot.

## What is live on `main`

- **`gauntlet`:** repeated builder and critic rounds against a bar, with blind comparison
- **`private-words`:** keeps private words out of a repo, with a list held outside every repo
- **`adversarial-review`:** a hostile expert panel attacks one or
  more items against audiences, styles, standards and obligations by region, phase and industry.
  The user confirms the panel first, and any lens they ask for always runs
- **The gate:** pull requests only, rebase merges only, and `checks` and `lint` must pass.
  Links are checked locally, not in CI: `python3 scripts/links.py`
- **Automatic review and merge:** `review.yml` has an
  automated reviewer read each pull request against AGENTS.md, post one comment, and fail on a
  BLOCK verdict. `auto-merge.yml` turns on rebase auto-merge for the owner's own non-draft pull
  requests, so GitHub merges once every required check passes. It needs three owner settings:
  an `ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN` secret, "Allow auto-merge", and `review`
  added to the `main: CI must pass` ruleset. A merge made by the workflow token does not start
  the `push` run of CI on `main`, so `main` is checked only through its pull requests
- **Clean installs work:** `gauntlet` and `private-words` were installed from GitHub into an empty configuration

## Do this first

**Bring [pull request 8](https://github.com/rogerbucks/skillknot/pull/8) up to date.** It adds
eleven plugins, and it is a draft that cannot merge yet.

1. **Resolve the conflicts.** `private-words` changed `marketplace.json`, `README.md` and
   `reviewed-powers.json`, which that branch changes too
2. **Keep both sides of `reviewed-powers.json`.** It is a list of reviewed powers, so no entry may
   be dropped to settle a conflict
3. **Get CI running.** The pull request shows no checks at all, so nothing there has passed the
   gate yet. Its test count of 51 also predates the 84 now on `main`
4. **Split it if review stalls.** Hooks that can stop or allow an agent's actions deserve their own
   review, so `claude-code-guards` is the natural piece to take apart first
5. **Run the stranger dry-run on each skill.** That pull request says each had a paper dry-run and
   no live one. Paper runs earn their keep: the one for `private-words` found a word leaking
   through a printed file name, and a failed history scan that reported clean

Pull request 8 was not reviewed for this handover. Everything above comes from its description and
its file list.

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
