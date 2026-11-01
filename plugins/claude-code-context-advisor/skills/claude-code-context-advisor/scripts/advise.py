#!/usr/bin/env python3
"""Reads one Claude Code session record and reports how its context was spent: big files read in
full, files read again unchanged, heavy tool output, how full the context is, and where a subagent
or a cheaper model would have done.

Usage:
  python3 advise.py --latest            the newest session for the current folder
  python3 advise.py --latest DIR        the newest session for DIR
  python3 advise.py PATH.jsonl          one session record
Options: --window N (context size in tokens, default 200000), --json (machine-readable output).
Writes: nothing. It reads the record and prints a report. It never prints file contents, only
names, counts, sizes and the start of a shell command.

Sizes are estimates: about 4 characters to a token. The context figure comes from the last reply's
own token counts when the record has them.
"""

import argparse
import json
import sys
from pathlib import Path

CHARS_PER_TOKEN = 4
BIG_READ = 8_000
BIG_OUTPUT = 10_000
SEARCH_RUN = 15
SEARCH_TOOLS = {"Read", "Grep", "Glob", "WebSearch", "WebFetch"}
EDIT_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
ROUTINE_BASH = (
    "ls",
    "cat",
    "head",
    "tail",
    "wc",
    "pwd",
    "git status",
    "git log",
    "git diff",
)


def tokens(chars):
    return max(1, chars // CHARS_PER_TOKEN)


def text_size(content):
    """Characters of text in a tool result, which may be a string or a list of parts."""
    if isinstance(content, str):
        return len(content)
    if isinstance(content, list):
        return sum(
            len(part.get("text", "")) for part in content if isinstance(part, dict)
        )
    return 0


def latest_record(folder):
    slug = str(Path(folder).resolve()).replace("/", "-").replace(".", "-")
    project = Path.home() / ".claude" / "projects" / slug
    records = sorted(project.glob("*.jsonl"), key=lambda p: p.stat().st_mtime)
    if not records:
        raise SystemExit(f"No session record found for {folder}")
    return records[-1]


def entries(path):
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        try:
            entry = json.loads(raw)
        except ValueError:
            continue
        if isinstance(entry, dict) and not entry.get("isSidechain"):
            yield entry


def is_compaction(entry):
    return entry.get("subtype") == "compact_boundary" or bool(
        entry.get("isCompactSummary")
    )


def collect(path):
    """One pass over the record. Returns the calls in order, and the last context reading."""
    calls, pending, last_usage = [], {}, None
    compactions = 0
    for entry in entries(path):
        if is_compaction(entry):
            compactions += 1
            calls.append({"name": "(compaction)", "input": {}, "size": 0})
            continue
        message = entry.get("message") or {}
        if entry.get("type") == "assistant" and isinstance(message.get("usage"), dict):
            last_usage = message["usage"]
        content = message.get("content")
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_use":
                call = {
                    "name": block.get("name", ""),
                    "input": block.get("input") or {},
                    "size": 0,
                }
                pending[block.get("id")] = call
                calls.append(call)
            elif (
                block.get("type") == "tool_result"
                and block.get("tool_use_id") in pending
            ):
                pending[block["tool_use_id"]]["size"] = text_size(block.get("content"))
    return calls, last_usage, compactions


def context_used(usage):
    if not usage:
        return None
    return sum(
        usage.get(key) or 0
        for key in (
            "input_tokens",
            "cache_read_input_tokens",
            "cache_creation_input_tokens",
        )
    )


def label(call):
    data = call["input"]
    return (
        data.get("file_path")
        or data.get("path")
        or data.get("url")
        or data.get("pattern")
        or (data.get("command") or "")[:60]
        or call["name"]
    )


def where(call):
    name, target = call["name"], label(call)
    return f"`{name}`" if target == name else f"`{name}` on `{target}`"


def analyse(calls, usage, compactions, window):
    findings = []
    since_compaction = []
    for call in calls:
        if call["name"] == "(compaction)":
            since_compaction = []
        else:
            since_compaction.append(call)

    big_reads = [
        c
        for c in since_compaction
        if c["name"] == "Read"
        and tokens(c["size"]) >= BIG_READ
        and not {"offset", "limit"} & set(c["input"])
    ]
    for call in big_reads:
        findings.append(
            (
                tokens(call["size"]),
                "Big file read in full",
                (
                    f"`{label(call)}` (~{tokens(call['size']):,} tokens). Next time, search it first and "
                    "read only the section you need, with a line offset and limit."
                ),
            )
        )

    seen, changed = {}, set()
    for call in since_compaction:
        target = call["input"].get("file_path")
        if not target:
            continue
        if call["name"] in EDIT_TOOLS:
            changed.add(target)
        elif call["name"] == "Read":
            if target in seen and target not in changed:
                seen[target]["again"] += tokens(call["size"])
            else:
                seen.setdefault(target, {"again": 0})
                changed.discard(target)
    for target, info in seen.items():
        if info["again"]:
            findings.append(
                (
                    info["again"],
                    "Read again, unchanged",
                    (
                        f"`{target}` was read more than once with no edit between (~{info['again']:,} "
                        "tokens repeated). The first read is still in context: refer back to it."
                    ),
                )
            )

    for call in since_compaction:
        if call["name"] != "Read" and tokens(call["size"]) >= BIG_OUTPUT:
            findings.append(
                (
                    tokens(call["size"]),
                    "Heavy tool output",
                    (
                        f"{where(call)} returned ~{tokens(call['size']):,} tokens. "
                        "Filter it at the source: a narrower search, fewer lines, or a quiet flag."
                    ),
                )
            )

    run = longest = 0
    for call in since_compaction:
        run = run + 1 if call["name"] in SEARCH_TOOLS else 0
        longest = max(longest, run)
    if longest >= SEARCH_RUN:
        findings.append(
            (
                longest * 500,
                "Long search run",
                (
                    f"{longest} searches and reads in a row with no other step. A research subagent would do "
                    "this in its own context and hand back only the answer."
                ),
            )
        )

    routine = sum(
        1
        for c in since_compaction
        if c["name"] in {"Glob", "Grep"}
        or (
            c["name"] == "Bash"
            and (c["input"].get("command") or "").strip().startswith(ROUTINE_BASH)
        )
    )
    if since_compaction and routine / len(since_compaction) >= 0.5 and routine >= 20:
        findings.append(
            (
                routine * 100,
                "Mostly routine steps",
                (
                    f"{routine} of {len(since_compaction)} steps were routine lookups. A fast, cheaper "
                    "model or a subagent could take these. See the model-picker skill for how to test that."
                ),
            )
        )

    used = context_used(usage)
    advice = None
    if used:
        share = used / window
        if share >= 0.8:
            advice = "Context is over 80% full. Run a handoff, then compact or start a fresh session now."
        elif share >= 0.6:
            advice = (
                "Context is over 60% full. Plan to compact at the next natural break."
            )
        else:
            advice = "Context has room. No need to compact yet."
    findings.sort(key=lambda f: -f[0])
    return {
        "context_tokens": used,
        "window": window,
        "compactions": compactions,
        "steps": len(since_compaction),
        "advice": advice,
        "findings": [
            {"kind": kind, "tokens": size, "detail": detail}
            for size, kind, detail in findings
        ],
    }


def report(result):
    lines = ["# Context advice", ""]
    used, window = result["context_tokens"], result["window"]
    if used:
        lines.append(
            f"**{result['advice']}** About {used:,} of {window:,} tokens in use ({used * 100 // window}%)."
        )
    else:
        lines.append(
            "**The record has no token counts,** so how full the context is cannot be told."
        )
    lines.append("")
    lines.append(
        f"Steps since the last compaction: {result['steps']}. Compactions so far: {result['compactions']}."
    )
    lines.append("")
    if not result["findings"]:
        lines.append(
            "Nothing to fix: no big whole-file reads, repeats or heavy outputs found."
        )
        return "\n".join(lines)
    lines += ["| What | Tokens | Advice |", "| --- | --- | --- |"]
    for f in result["findings"][:15]:
        lines.append(f"| {f['kind']} | ~{f['tokens']:,} | {f['detail']} |")
    if len(result["findings"]) > 15:
        lines.append(f"\n{len(result['findings']) - 15} smaller findings not shown.")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("record", nargs="?", help="a session record (.jsonl)")
    parser.add_argument("--latest", nargs="?", const=".", metavar="DIR")
    parser.add_argument("--window", type=int, default=200_000)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if args.latest is not None:
        path = latest_record(args.latest)
    elif args.record:
        path = Path(args.record)
    else:
        parser.error("give a session record, or --latest")
    result = analyse(*collect(path), args.window)
    print(json.dumps(result, indent=2) if args.json else report(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
