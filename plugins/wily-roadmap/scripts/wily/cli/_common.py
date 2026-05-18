"""Shared CLI primitives for Wily v3."""

from __future__ import annotations

import json
import sys
from typing import Any

EXIT_OK = 0
EXIT_FAILURE = 1
EXIT_USAGE = 2
EXIT_TRANSITION = 3

COMMANDS = (
    "init",
    "next",
    "claim",
    "go",
    "done",
    "block",
    "replan",
    "land",
    "watch",
    "status",
)

REMOVED_COMMANDS = {
    "run": "Use 'wily claim <id>' + 'wily go <id>' instead.",
    "retry": "Task attempts are managed by custom-workflow, not Wily v3.",
    "decompose" + "-stage": "Wily v3 has no hierarchical decomposition.",
    "issues": "GitHub Issues integration is not part of Wily v3.",
    "clean": "Wily v3 has no broad cleanup command.",
    "update": "Use the plugin marketplace update flow.",
    "start": "Use 'wily claim <id>'.",
    "complete": "Use 'wily done <id>'.",
    "bo" + "ard": "Wily v3 has no external dashboard integration.",
    "live" + "-heartbeat": "Wily v3 has no live bridge.",
    "live" + "-worked": "Wily v3 has no live bridge.",
    "live" + "-event": "Wily v3 has no live bridge.",
}


def emit_text(message: str) -> None:
    print(message)


def emit_json(payload: Any) -> None:
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def emit_error(message: str) -> None:
    print(message, file=sys.stderr)


def print_help() -> None:
    emit_text("wily v3 - Project + flat goal-sized Task manager")
    emit_text("")
    emit_text("Usage: wily <command> [args]")
    emit_text("")
    emit_text("Commands:")
    for command in COMMANDS:
        emit_text(f"  {command}")
