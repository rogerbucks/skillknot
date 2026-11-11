#!/usr/bin/env python3
"""Governs connector tools on the agent's side: asks before anything is sent, shared or deleted
through a connector, and, once messages or mail have been read this session, asks before any tool
that could carry text out.

Usage: a PreToolUse hook on every tool (see ../hooks/hooks.json). To try it by hand:
  echo '{"tool_name":"mcp__mail__send_email","tool_input":{},"session_id":"t"}' | python3 connector_guard.py
Writes: one empty marker file per session in the system temp folder, once untrusted messages are read.

Why the second rule: a message can carry hidden instructions. This stops one from steering a read
straight into a leak without a person seeing it. Turn it off with "off": ["connector"] in the overlay.

Trusted servers: "connector_trusted_servers": ["name"] in the overlay stops both asks for that MCP
server's own tools, for example a chat surface whose posts go only to its own user. Reads through it
still count as reading messages, so a later outbound call from another tool still asks.
"""

import hashlib
import os
import re
import sys
import tempfile

from guardlib import run

ALWAYS_ASK = re.compile(
    r"(^|_)(send|forward|reply|rsvp|post|publish|share|delete|trash|remove|transfer|pay|invoice)(_|$)",
    re.IGNORECASE,
)
READ_VERB = re.compile(r"(^|_)(read|get|search|list|fetch)(_|$)", re.IGNORECASE)
MESSAGE_NOUN = re.compile(
    r"(mail|email|message|thread|inbox|chat|conversation|imessage|sms|dm)",
    re.IGNORECASE,
)
OUTBOUND_TOOLS = {"WebFetch", "WebSearch"}
OUTBOUND_VERB = re.compile(
    r"(^|_)(navigate|open_url|upload|create_file|create_issue|comment|draft)(_|$)",
    re.IGNORECASE,
)


def server(tool):
    """The MCP server's name in mcp__<server>__<tool>, or None for a built-in tool."""
    match = re.match(r"^mcp__(.+?)__.+$", tool)
    return match.group(1) if match else None


def leaf(tool):
    """The tool's own name, after mcp__<server>__."""
    match = re.match(r"^mcp__.+?__(.+)$", tool)
    return match.group(1) if match else tool


def marker(session_id):
    digest = hashlib.sha256((session_id or "none").encode()).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), f"skillknot-connector-read-{digest}")


def decide(event, config):
    tool = event.get("tool_name", "")
    session = event.get("session_id", "")
    name = leaf(tool)
    is_mcp = tool.startswith("mcp__")
    if is_mcp and server(tool) in config.get("connector_trusted_servers", []):
        if READ_VERB.search(name) and MESSAGE_NOUN.search(name):
            open(marker(session), "a").close()
        return None
    if is_mcp and ALWAYS_ASK.search(name):
        return (
            "ask",
            f"Connector guard: `{name}` sends, shares or removes something outside this machine. Approve it this once?",
        )
    if is_mcp and READ_VERB.search(name) and MESSAGE_NOUN.search(name):
        open(marker(session), "a").close()
        return None
    if os.path.exists(marker(session)) and (
        tool in OUTBOUND_TOOLS or (is_mcp and OUTBOUND_VERB.search(name))
    ):
        return "ask", (
            f"Connector guard: messages were read earlier in this session, and `{name}` could carry their "
            "text out. Check that this call is yours, not an instruction found inside a message."
        )
    return None


if __name__ == "__main__":
    sys.exit(run("connector", decide))
