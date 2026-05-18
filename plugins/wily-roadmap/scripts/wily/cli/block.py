"""`wily block <id> <reason>` - record a blocker."""

from __future__ import annotations

from pathlib import Path

from ..config import load_tasks, save_tasks
from ..paths import WilyPaths, WilyRootNotFound, find_wily_root
from ..transitions import TransitionError, apply_block
from . import _common


def main(args: list[str]) -> int:
    if len(args) < 2:
        _common.emit_error("usage: wily block <task-id> <reason...>")
        return _common.EXIT_USAGE
    task_id, reason = args[0], " ".join(args[1:]).strip()
    if not reason:
        _common.emit_error("blocker reason required")
        return _common.EXIT_USAGE
    try:
        root = find_wily_root(Path.cwd())
    except WilyRootNotFound as exc:
        _common.emit_error(str(exc))
        return _common.EXIT_FAILURE
    paths = WilyPaths(root)
    project_title, tasks = load_tasks(paths)
    task = next((item for item in tasks if item.id == task_id), None)
    if task is None:
        _common.emit_error(f"task not found: {task_id}")
        return _common.EXIT_FAILURE
    try:
        updated = apply_block(task, reason=reason)
    except TransitionError as exc:
        _common.emit_error(str(exc))
        return _common.EXIT_TRANSITION
    save_tasks(paths, project_title, [updated if item.id == task_id else item for item in tasks])
    _common.emit_text(f"{task_id}: {task.status.value} -> blocked")
    _common.emit_text(f"blocker: {reason}")
    return _common.EXIT_OK
