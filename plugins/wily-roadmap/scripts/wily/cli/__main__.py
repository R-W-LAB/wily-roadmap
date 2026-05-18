"""Entry dispatch for Wily v3."""

from __future__ import annotations

import sys
from typing import Callable

from . import _common


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        _common.print_help()
        return _common.EXIT_USAGE
    if args[0] in {"-h", "--help"}:
        _common.print_help()
        return _common.EXIT_OK
    command, rest = args[0], args[1:]
    if command in {"live" + "-worked", "live" + "-heartbeat", "live" + "-event"}:
        if "--from-hook" in rest:
            return _common.EXIT_OK
    if command in _common.REMOVED_COMMANDS:
        _common.emit_error(
            f"Error: {command!r} is removed in wily v3. {_common.REMOVED_COMMANDS[command]}"
        )
        return _common.EXIT_USAGE
    handler = _load_handler(command)
    if handler is None:
        _common.emit_error(f"unknown command: {command!r}")
        _common.emit_error(f"available: {', '.join(_common.COMMANDS)}")
        return _common.EXIT_USAGE
    return handler(rest)


def _load_handler(command: str) -> Callable[[list[str]], int] | None:
    if command not in _common.COMMANDS:
        return None
    module = __import__(f"wily.cli.{command}", fromlist=["main"])
    return getattr(module, "main", None)


if __name__ == "__main__":
    raise SystemExit(main())
