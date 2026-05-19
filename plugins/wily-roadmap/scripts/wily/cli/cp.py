"""`wily cp` - record task checkpoint progress."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from ..config import load_actors, load_tasks
from ..models import Task
from ..observation import git_config_identity, match_actor
from ..paths import WilyPaths, WilyRootNotFound, find_wily_root, touch_wily
from ..progress import CpEvent, append_event, append_event_once, parse_status_board
from . import _common

DESCRIPTION = "record task checkpoint progress"
USAGE = "usage: wily cp <task-id> <start|done|note|import-status> <cp-or-status-path> [--actor <id>] [--note <text>] [--ts <iso>] [--dry-run] [--json]"
HELP = "\n".join(
    [
        "Options:",
        "  --actor <id>  override the checkpoint actor",
        "  --note <text> attach a checkpoint note",
        "  --ts <iso>    override event timestamp",
        "  --dry-run     parse import-status without writing events",
        "  --json        emit the event as JSON",
    ]
)


def main(args: list[str]) -> int:
    args, as_json = _common.consume_json_flag(args)
    missing = _common.missing_value_flag(args, {"--actor", "--note", "--ts"})
    if missing:
        _common.emit_error(f"{missing} requires a value")
        return _common.EXIT_USAGE
    positional = _common.positionals(args, value_flags={"--actor", "--note", "--ts"})
    if len(positional) < 2:
        _common.emit_error("usage: wily cp <task-id> <start|done|note|import-status> <cp-or-status-path> [--actor <id>] [--note <text>] [--ts <iso>]")
        return _common.EXIT_USAGE
    task_id, event_or_import = positional[0], positional[1]
    value = positional[2] if len(positional) >= 3 else None
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
    actor = _actor_id(root, paths, task, _common.extract_value(args, "--actor"))
    ts = _common.extract_value(args, "--ts") or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if event_or_import == "import-status":
        return _import_status(root, paths, task_id, value, actor=actor, ts=ts, dry_run="--dry-run" in args)
    if value is None:
        _common.emit_error("usage: wily cp <task-id> <start|done|note|import-status> <cp-or-status-path> [--actor <id>] [--note <text>] [--ts <iso>]")
        return _common.EXIT_USAGE
    if event_or_import not in {"start", "done", "note"}:
        _common.emit_error("cp event must be one of: start, done, note, import-status")
        return _common.EXIT_USAGE
    event = CpEvent(
        ts=ts,
        actor=actor,
        cp=value,
        event=event_or_import,  # type: ignore[arg-type]
        note=_common.extract_value(args, "--note"),
    )
    if event.event == "note":
        append_event(paths, task_id, event)
        created = True
    else:
        created = append_event_once(paths, task_id, event)
    touch_wily(paths)
    if as_json:
        _common.emit_json({"task_id": task_id, "event": event.__dict__, "created": created})
        return _common.EXIT_OK
    _common.emit_text(f"{task_id} cp {event.event}: {event.cp}{'' if created else ' (already recorded)'}")
    return _common.EXIT_OK


def _import_status(root: Path, paths: WilyPaths, task_id: str, value: str | None, *, actor: str, ts: str, dry_run: bool = False) -> int:
    source = _status_source(root, paths, task_id, value)
    try:
        text = source.read_text(encoding="utf-8")
    except OSError as exc:
        _common.emit_error(f"cannot read status board: {exc}")
        return _common.EXIT_FAILURE
    events, unrecognized = parse_status_board(text, actor=actor, ts=ts)
    for line in unrecognized:
        _common.emit_error(f"unrecognized status line: {line}")
    if dry_run:
        _common.emit_text(f"{task_id} cp import-status dry-run: {len(events)} event(s) from {source.relative_to(root) if source.is_relative_to(root) else source}")
        return _common.EXIT_OK
    created = 0
    for event in events:
        if append_event_once(paths, task_id, event):
            created += 1
    touch_wily(paths)
    _common.emit_text(f"{task_id} cp import-status: {created} event(s) from {source.relative_to(root) if source.is_relative_to(root) else source}")
    return _common.EXIT_OK


def _status_source(root: Path, paths: WilyPaths, task_id: str, value: str | None) -> Path:
    if value is None:
        return paths.handoff_status_md(task_id)
    candidate = Path(value)
    if candidate.is_absolute():
        return candidate
    root_candidate = (root / candidate).resolve()
    if root_candidate.exists():
        return root_candidate
    handoff_candidate = paths.handoff_dir(task_id) / candidate
    if handoff_candidate.exists():
        return handoff_candidate
    return root_candidate


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
