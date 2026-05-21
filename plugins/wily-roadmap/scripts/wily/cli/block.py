"""`wily block <id> <reason>` - record a blocker."""

from __future__ import annotations

from pathlib import Path

from .. import board_runtime
from ..config import load_tasks, save_tasks
from ..paths import WilyPaths, WilyRootNotFound, find_wily_root, touch_wily
from ..transitions import TransitionError, apply_block
from . import _common

DESCRIPTION = "record a blocker on a task"
USAGE = "usage: wily block <task-id> <reason...> [--json]"
HELP = "\n".join(
    [
        "Options:",
        "  --json  emit the updated task as JSON",
    ]
)


def main(args: list[str]) -> int:
    args, as_json = _common.consume_json_flag(args)
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
    board_config = board_runtime.project_config_for_root(root)
    config_error = board_runtime.config_error(board_config)
    if config_error:
        _common.emit_error(config_error)
        return _common.EXIT_FAILURE
    if board_runtime.authority_enabled(board_config):
        result = board_runtime.transition_task(
            board_config,
            board_config.repo,
            task_id,
            "block",
            {"reason": reason},
        )
        if result.get("sent") is False:
            _common.emit_error(board_runtime.board_failure_message(result))
            return _common.EXIT_FAILURE
        updated = board_runtime.apply_runtime_response(updated, result)
    save_tasks(paths, project_title, [updated if item.id == task_id else item for item in tasks])
    touch_wily(paths)
    if as_json:
        _common.emit_json({"task": updated.to_dict()})
        return _common.EXIT_OK
    _common.emit_text(f"{task_id}: {task.status.value} -> blocked")
    _common.emit_text(f"blocker: {reason}")
    return _common.EXIT_OK
