"""`wily watch` - polling loop around the status renderer."""

from __future__ import annotations

import time

from . import _common
from .status import main as status_main


def main(args: list[str]) -> int:
    once = "--once" in args
    interval = _interval(args)
    if interval is None:
        return _common.EXIT_USAGE
    status_args = _remove_interval([arg for arg in args if arg != "--once"])
    while True:
        rc = status_main(status_args)
        if once:
            return rc
        try:
            time.sleep(interval)
        except KeyboardInterrupt:
            return _common.EXIT_OK


def _interval(args: list[str]) -> float | None:
    if "--interval" not in args:
        return 2.0
    index = args.index("--interval")
    if index + 1 >= len(args):
        _common.emit_error("--interval requires a value")
        return None
    try:
        value = float(args[index + 1])
    except ValueError:
        _common.emit_error("--interval value must be a number")
        return None
    if value <= 0:
        _common.emit_error("--interval must be positive")
        return None
    return value


def _remove_interval(args: list[str]) -> list[str]:
    out: list[str] = []
    skip = False
    for arg in args:
        if skip:
            skip = False
            continue
        if arg == "--interval":
            skip = True
            continue
        out.append(arg)
    return out
