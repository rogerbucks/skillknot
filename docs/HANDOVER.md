# Handover

Where SkillKnot stands, and what comes next. Date: 1 Nov 2026. Follow [AGENTS.md](../AGENTS.md)
throughout. This file holds the reasoning that the code cannot.

## What is live on `main`

- **`gauntlet`:** repeated builder and critic rounds against a bar, with blind comparison
- **`private-words`:** keeps private words out of a repo, with a list held outside every repo
- **The gate:** pull requests only, rebase merges only, and `checks` and `lint` must pass. The
  `links` job reports but does not block
- **Clean installs work:** both skills were installed from GitHub into an empty configuration

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
