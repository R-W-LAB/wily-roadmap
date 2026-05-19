"""Shared CLI primitives for Wily v3."""

from __future__ import annotations

import json
import sys
from typing import Any

from .. import i18n

EXIT_OK = 0
EXIT_FAILURE = 1
EXIT_USAGE = 2
EXIT_TRANSITION = 3

COMMANDS = (
    "init",
    "next",
    "claim",
    "cp",
    "go",
    "done",
    "block",
    "agent",
    "replan",
    "land",
    "watch",
    "status",
    "doctor",
)

REMOVED_COMMANDS = {
    "run": "Use 'wily claim <id>' + 'wily go <id>' instead.",
    "retry": "Task attempts are managed by custom-workflow, not Wily v3.",
    "decompose-stage": "Wily v3 has no hierarchical decomposition.",
    "issues": "GitHub Issues integration is not part of Wily v3.",
    "clean": "Wily v3 has no broad cleanup command.",
    "update": "Use the plugin marketplace update flow.",
    "start": "Use 'wily claim <id>'.",
    "complete": "Use 'wily done <id>'.",
    "board": "Wily v3 has no external dashboard integration.",
    "live-heartbeat": "Wily v3 has no live bridge.",
    "live-worked": "Wily v3 has no live bridge.",
    "live-event": "Wily v3 has no live bridge.",
}


def emit_text(message: str) -> None:
    print(message)


def emit_json(payload: Any) -> None:
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def emit_error(message: str) -> None:
    print(message, file=sys.stderr)


def consume_json_flag(args: list[str]) -> tuple[list[str], bool]:
    return [arg for arg in args if arg != "--json"], "--json" in args


def extract_value(args: list[str], flag: str) -> str | None:
    for index, arg in enumerate(args):
        if arg == flag and index + 1 < len(args):
            return args[index + 1]
        if arg.startswith(flag + "="):
            return arg.split("=", 1)[1]
    return None


def extract_values(args: list[str], flag: str) -> list[str]:
    values: list[str] = []
    for index, arg in enumerate(args):
        if arg == flag and index + 1 < len(args):
            values.append(args[index + 1])
        elif arg.startswith(flag + "="):
            values.append(arg.split("=", 1)[1])
    return values


def missing_value_flag(args: list[str], flags: set[str]) -> str | None:
    for index, arg in enumerate(args):
        if arg in flags and (index + 1 >= len(args) or args[index + 1].startswith("--")):
            return arg
    return None


def positionals(args: list[str], *, value_flags: set[str] | None = None) -> list[str]:
    value_flags = value_flags or set()
    result: list[str] = []
    skip_next = False
    for arg in args:
        if skip_next:
            skip_next = False
            continue
        if arg in value_flags:
            skip_next = True
            continue
        if any(arg.startswith(flag + "=") for flag in value_flags):
            continue
        if not arg.startswith("--"):
            result.append(arg)
    return result


def print_help() -> None:
    emit_text(i18n.text("title"))
    emit_text("")
    emit_text(i18n.text("usage"))
    emit_text("  wily <command> [args]")
    emit_text("  wily help <command>")
    emit_text("")
    emit_text(i18n.text("commands"))
    for command in COMMANDS:
        description = command_description(command)
        suffix = f"  {description}" if description else ""
        emit_text(f"  {command:<8}{suffix}")


def command_description(command: str) -> str:
    module = _load_command_module(command)
    if module is None:
        return ""
    fallback = str(getattr(module, "DESCRIPTION", "")).strip()
    return i18n.command_description(command, fallback)


def print_command_help(command: str) -> int:
    if command in REMOVED_COMMANDS:
        emit_error(i18n.text("removed", command=command, detail=REMOVED_COMMANDS[command]))
        return EXIT_USAGE
    if command not in COMMANDS:
        emit_error(i18n.text("unknown", command=command))
        emit_error(i18n.text("available", commands=", ".join(COMMANDS)))
        return EXIT_USAGE
    module = _load_command_module(command)
    if module is None:
        emit_error(f"unknown command: {command!r}")
        return EXIT_USAGE
    description = str(getattr(module, "DESCRIPTION", "")).strip()
    description = i18n.command_description(command, description)
    usage = str(getattr(module, "USAGE", "")).strip()
    help_text = str(getattr(module, "HELP", "")).strip()
    if description:
        emit_text(f"wily {command} - {description}")
        emit_text("")
    if usage:
        emit_text(i18n.text("usage"))
        emit_text(usage)
    if help_text:
        emit_text("")
        emit_text(_localized_help_text(help_text))
    return EXIT_OK


def _load_command_module(command: str):
    if command not in COMMANDS:
        return None
    try:
        return __import__(f"wily.cli.{command}", fromlist=["DESCRIPTION", "USAGE", "HELP"])
    except Exception:
        return None


def _localized_help_text(help_text: str) -> str:
    return (
        help_text.replace("Options:", i18n.text("options"))
        .replace("Commands:", i18n.text("commands"))
    )
