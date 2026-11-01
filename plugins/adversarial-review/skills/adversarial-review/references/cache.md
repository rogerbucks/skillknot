# How standards are cached and refreshed

The standards files hold **links, not copies.** Laws and standards change, and a copy goes stale
without warning. Each row keeps a short cached note (version, dates, what to check) and the date
the link was last confirmed, so a review can run fast and still know how old its facts are.

## Two layers

1. **The registry** in [standards/](standards/global.md), in this skill. Read-only once installed.
   Its **Checked** column is the date the maintainer last opened the link and confirmed the note
2. **The local cache** at `~/.cache/skillknot/adversarial-review/standards.md`, written by each
   review. It overrides the registry for any ID it holds, and is never committed

The local cache has one row per ID:

```text
| ID | Link used | Title seen | Version or as-of | What changed | Checked |
```

## Weekly rule

At Stage 3, for each standard on the panel only:

1. **Find its newest Checked date** across the local cache and the registry
2. **7 days old or less:** use it as cached. Do not fetch
3. **Older than 7 days, or *never*:** open the link. Confirm the title, the current version or
   compilation date, and any amendment, delay or replacement notice on the page
4. **Write the result** to the local cache with today's date, even if nothing changed
5. **If the page moved,** follow the redirect, record the new link, and list it under *Registry
   updates* in the report
6. **If the page cannot be read** (blocked, down, or rendered by script), keep the cached note,
   mark the standard *unverified since {date}*, and say so beside each finding that rests on it

**Never fill a gap from memory.** A version or date that no page confirmed is written as
*not confirmed*.

**With no web access,** skip the fetch, mark every stale standard *unverified since {date}*, and
put that at the top of the report.

**With no writable home folder,** keep the cache rows in the review folder at
`.adversarial-review/<review-slug>/standards-cache.md`.

## Keeping the registry itself fresh

The repository runs a weekly link check over every standards file. A dead link opens nothing by
itself: the maintainer reads the result, confirms the new location, and updates the row and its
Checked date in a pull request. A review that finds a registry update says so in its report, so
the user can send it upstream.
