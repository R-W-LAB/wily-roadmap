"""`wily cp` - record task checkpoint progress."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from ..config import load_actors, load_tasks
from ..models import Task
from ..observation import git_config_identity, match_actor
from ..paths import WilyPaths, WilyRootNotFound, find_wily_root
from ..progress import CpEvent, append_event, append_event_once, events_from_status_board
from . import _common


def main(args: list[str]) -> int:
    positional = _positionals(args, value_flags={"--actor", "--note", "--ts"})
    if len(positional) < 3:
        _common.emit_error("usage: wily cp <task-id> <start|done|note|import-status> <cp-or-status-path> [--actor <id>] [--note <text>] [--ts <iso>]")
        return _common.EXIT_USAGE
    task_id, event_or_import, value = positional[0], positional[1], positional[2]
    try:
        root = find_wily_root(Path.cwd())
    except WilyRootNotFound as exc:
        _common.emit_error(str(exc))
        return _common.EXIT_FAILURE
    paths = WilyPaths(root)
    _, tasks = load_tasks(paths)
    task = next((item for item in tasks if item.id == task_id), None)
    if task is None:
        _common.emit_error(f"task not found: {task_id}")
        return _common.EXIT_FAILURE
    actor = _actor_id(root, paths, task, _extract_value(args, "--actor"))
    ts = _extract_value(args, "--ts") or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if event_or_import == "import-status":
        return _import_status(root, paths, task_id, value, actor=actor, ts=ts)
    if event_or_import not in {"start", "done", "note"}:
        _common.emit_error("cp event must be one of: start, done, note, import-status")
        return _common.EXIT_USAGE
    event = CpEvent(
        ts=ts,
        actor=actor,
        cp=value,
        event=event_or_import,  # type: ignore[arg-type]
        note=_extract_value(args, "--note"),
    )
    if event.event == "note":
        append_event(paths, task_id, event)
        created = True
    else:
        created = append_event_once(paths, task_id, event)
    _common.emit_text(f"{task_id} cp {event.event}: {event.cp}{'' if created else ' (already recorded)'}")
    return _common.EXIT_OK


def _import_status(root: Path, paths: WilyPaths, task_id: str, value: str, *, actor: str, ts: str) -> int:
    source = (root / value).resolve() if not Path(value).is_absolute() else Path(value)
    try:
        text = source.read_text(encoding="utf-8")
    except OSError as exc:
        _common.emit_error(f"cannot read status board: {exc}")
        return _common.EXIT_FAILURE
    created = 0
    for event in events_from_status_board(text, actor=actor, ts=ts):
        if append_event_once(paths, task_id, event):
            created += 1
    _common.emit_text(f"{task_id} cp import-status: {created} event(s) from {source.relative_to(root) if source.is_relative_to(root) else source}")
    return _common.EXIT_OK


def _actor_id(root: Path, paths: WilyPaths, task: Task, explicit: str | None) -> str:
    if explicit:
        return explicit
    if task.actor:
        return task.actor
    if task.assignee:
        return task.assignee
    email, name = git_config_identity(root)
    actor = match_actor(load_actors(paths), email=email, name=name)
    return actor.id if actor else "unknown"


def _extract_value(args: list[str], flag: str) -> str | None:
    if flag not in args:
        return None
    index = args.index(flag)
    return args[index + 1] if index + 1 < len(args) else None


def _positionals(args: list[str], *, value_flags: set[str]) -> list[str]:
    out: list[str] = []
    skip = False
    for arg in args:
        if skip:
            skip = False
            continue
        if arg in value_flags:
            skip = True
            continue
        if not arg.startswith("--"):
            out.append(arg)
    return out
