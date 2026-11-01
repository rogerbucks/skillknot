---
name: private-words
description: Use when the user wants to keep private words out of a repo, add to or review a private word list, scan a repo or its history for them, load them into CI, or a private word has turned up in a file or commit.
license: MIT
compatibility: Needs Python 3 and Git. Loading a CI secret needs the GitHub CLI.
---

# private-words: keep a person's private words out of a repo

**The words live in one place, which the user chooses, outside every repo.** Names, employers and
addresses are the usual ones. The list is the leak if it travels, so everything here works without
it being seen.

**Never read the list, and never write a word anywhere it could stay:** not in chat, a command, a
commit message, a file, a log or an issue. [scan.py](scripts/scan.py), in this skill's folder, reads the list for you.
If the user types a word in chat, it is in that transcript already, so say so and do not repeat it.

## Find the list

The script looks at `--list`, then `SKILLKNOT_TERMS_FILE`, then
`~/.config/skillknot/blocked-terms.md`, which may be a link to wherever the user keeps it.
`python3 scripts/scan.py --where` shows the path and the word count, and no word. If no list
exists, ask the user where it should live. The folder must be outside every Git repo, and should
be backed up. A password manager or a private notes folder suits it.

**The list is a Markdown note with a bullet per word,** and only bullets count, so notes around
them are safe:

```markdown
# Private words

- Example Employer
- Example Street
```

## What the user asks for

- **Add or change a word:** the user edits the list themselves. Give them the path and wait. Then
  rerun the scan, and load CI again if it uses the list
- **See the list:** give them the path to open, and the count, both from `--where`
- **Scan:** `python3 scripts/scan.py --repo <repo> --history`. History means authors, their
  emails, messages and every line a commit added. Add `--allow <word>` only for a longer public
  word that holds a private one, such as a handle, as it goes on the command line. Exit 0 is
  clean, 1 found something, and 2 means the scan could not run. It prints the reason, so pass
  that on and do not call the repo clean
- **Load CI:** `python3 scripts/scan.py --repo <repo> --set-secret LEAK_TERMS`. Only the words go,
  by standard input. Rerun it after every edit, as GitHub keeps its own copy. The workflow reads
  the secret and must print only where a word is, never which word. Other CI systems need the
  user to load the words themselves
- **Keep the list in the repo:** refuse, because a public repo with the list in it is the leak. Offer a
  private backup instead

## When a word turns up

The scan gives a file and line, or a commit, and no word. A file name holding a word shows as
`***`. **Stop before pushing anything else.**

- **Not yet pushed:** fix the file or the commit yourself, and scan again
- **Already public:** treat the word as seen. Tell the user before changing anything. Deleting it
  from the latest version leaves it in history, and rewriting history needs a force push, which is
  their call. Clones and forks keep the old text whatever happens
- **A credential:** this skill is the wrong tool. Revoke and replace it first

Fix wording by describing the place in general terms. Commit messages about the fix name no word.

## Rules for every run

- **A clean scan covers only the words on the list.** It cannot find a private word nobody added
- **If a guard blocks an action, stop and report it.** Never reword or re-encode around it
