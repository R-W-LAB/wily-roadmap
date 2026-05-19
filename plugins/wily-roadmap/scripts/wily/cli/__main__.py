"""Entry dispatch for Wily v3."""

from __future__ import annotations

import sys
from typing import Callable

from .. import i18n
from . import _common


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        _common.print_help()
        return _common.EXIT_USAGE
    if args[0] in {"-h", "--help"}:
        _common.print_help()
        return _common.EXIT_OK
    if args[0] == "help":
        if len(args) == 1:
            _common.print_help()
            return _common.EXIT_OK
        if len(args) == 2:
            return _common.print_command_help(args[1])
        _common.emit_error("usage: wily help <command>")
        return _common.EXIT_USAGE
    command, rest = args[0], args[1:]
    if command in {"live-worked", "live-heartbeat", "live-event"}:
        if "--from-hook" in rest:
            return _common.EXIT_OK
    if command in _common.REMOVED_COMMANDS:
        _common.emit_error(
            i18n.text("removed", command=command, detail=_common.REMOVED_COMMANDS[command])
        )
        return _common.EXIT_USAGE
    handler = _load_handler(command)
    if handler is None:
        _common.emit_error(i18n.text("unknown", command=command))
        _common.emit_error(i18n.text("available", commands=", ".join(_common.COMMANDS)))
        return _common.EXIT_USAGE
    if any(arg in {"-h", "--help"} for arg in rest):
        return _common.print_command_help(command)
    return handler(rest)


def _load_handler(command: str) -> Callable[[list[str]], int] | None:
    if command not in _common.COMMANDS:
        return None
    module = __import__(f"wily.cli.{command}", fromlist=["main"])
    return getattr(module, "main", None)


if __name__ == "__main__":
    raise SystemExit(main())
