"""`wily replan` - stage and commit task list edits."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from ..config import load_tasks, save_tasks
from ..models import Task, TaskStatus
from ..paths import WilyPaths, WilyRootNotFound, find_wily_root
from ..transitions import DependencyError, check_dependencies
from . import _common


def main(args: list[str]) -> int:
    try:
        root = find_wily_root(Path.cwd())
    except WilyRootNotFound as exc:
        _common.emit_error(str(exc))
        return _common.EXIT_FAILURE
    paths = WilyPaths(root)
    if not args or args[0] == "show":
        return _show(paths)
    sub, rest = args[0], args[1:]
    if sub == "add":
        return _add(paths, rest)
    if sub in {"revise", "revise-task"}:
        return _revise(paths, rest)
    if sub == "drop":
        return _drop(paths, rest)
    if sub == "assign":
        return _assign(paths, rest)
    if sub == "project":
        return _project(paths, rest)
    if sub == "commit":
        return _commit(paths)
    if sub == "cancel":
        return _cancel(paths)
    _common.emit_error(f"unknown replan subcommand: {sub}")
    return _common.EXIT_USAGE


def _load(paths: WilyPaths) -> dict[str, Any]:
    if paths.init_draft.exists():
        return yaml.safe_load(paths.init_draft.read_text(encoding="utf-8")) or {}
    return {"mode": "replan", "added": [], "edits": {}, "dropped": []}


def _save(paths: WilyPaths, draft: dict[str, Any]) -> None:
    paths.init_dir.mkdir(parents=True, exist_ok=True)
    paths.init_draft.write_text(
        yaml.safe_dump(draft, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def _show(paths: WilyPaths) -> int:
    title, tasks = load_tasks(paths)
    _common.emit_text(f"Project: {title}")
    for task in tasks:
        _common.emit_text(f"  {task.id} {task.status.value} {task.title}")
    if paths.init_draft.exists():
        _common.emit_text("(draft pending)")
    return _common.EXIT_OK


def _next_id(existing: list[str]) -> str:
    nums = [int(item[1:]) for item in existing if item.startswith("T") and item[1:].isdigit()]
    return f"T{(max(nums) + 1) if nums else 1:02d}"


def _add(paths: WilyPaths, args: list[str]) -> int:
    title = " ".join(args).strip()
    if not title:
        _common.emit_error("usage: wily replan add <title>")
        return _common.EXIT_USAGE
    _, tasks = load_tasks(paths)
    draft = _load(paths)
    task_id = _next_id([task.id for task in tasks] + [item["id"] for item in draft.get("added", [])])
    draft.setdefault("added", []).append(
        {"id": task_id, "title": title, "intent": "", "acceptance": "", "scope": [], "depends_on": [], "status": "ready"}
    )
    _save(paths, draft)
    _common.emit_text(f"draft: added {task_id} {title!r}")
    return _common.EXIT_OK


def _revise(paths: WilyPaths, args: list[str]) -> int:
    if len(args) < 3:
        _common.emit_error("usage: wily replan revise-task <id> <field> <value>")
        return _common.EXIT_USAGE
    task_id, field, value = args[0], args[1], " ".join(args[2:])
    if field not in {"title", "intent", "acceptance", "scope", "depends_on", "assignee"}:
        _common.emit_error("unsupported field")
        return _common.EXIT_USAGE
    parsed = _parse_value(field, value)
    draft = _load(paths)
    for item in draft.get("added", []):
        if item["id"] == task_id:
            item[field] = parsed
            _save(paths, draft)
            _common.emit_text(f"draft: {task_id}.{field} updated")
            return _common.EXIT_OK
    _, tasks = load_tasks(paths)
    task = next((item for item in tasks if item.id == task_id), None)
    if task is None:
        _common.emit_error(f"task not found: {task_id}")
        return _common.EXIT_FAILURE
    if task.status == TaskStatus.DONE and field != "title":
        _common.emit_error(f"{task_id} is done; refusing to revise {field}")
        return _common.EXIT_TRANSITION
    draft.setdefault("edits", {}).setdefault(task_id, {})[field] = parsed
    _save(paths, draft)
    _common.emit_text(f"draft: {task_id}.{field} updated")
    return _common.EXIT_OK


def _parse_value(field: str, value: str) -> Any:
    if field in {"scope", "depends_on"}:
        return [item.strip() for item in value.split(",") if item.strip()]
    return value


def _drop(paths: WilyPaths, args: list[str]) -> int:
    if len(args) != 1:
        _common.emit_error("usage: wily replan drop <task-id>")
        return _common.EXIT_USAGE
    task_id = args[0]
    _, tasks = load_tasks(paths)
    draft = _load(paths)
    task = next((item for item in tasks if item.id == task_id), None)
    if task and task.status != TaskStatus.READY:
        _common.emit_error(f"{task_id} is {task.status.value}; only ready tasks can be dropped")
        return _common.EXIT_TRANSITION
    if task:
        draft.setdefault("dropped", []).append(task_id)
    else:
        draft["added"] = [item for item in draft.get("added", []) if item["id"] != task_id]
    _save(paths, draft)
    _common.emit_text(f"draft: {task_id} dropped")
    return _common.EXIT_OK


def _assign(paths: WilyPaths, args: list[str]) -> int:
    if len(args) != 2:
        _common.emit_error("usage: wily replan assign <task-id> <actor>")
        return _common.EXIT_USAGE
    return _revise(paths, [args[0], "assignee", args[1]])


def _project(paths: WilyPaths, args: list[str]) -> int:
    title = " ".join(args).strip()
    if not title:
        _common.emit_error("usage: wily replan project <title>")
        return _common.EXIT_USAGE
    draft = _load(paths)
    draft["project_title"] = title
    _save(paths, draft)
    _common.emit_text("draft: project title updated")
    return _common.EXIT_OK


def _apply(paths: WilyPaths) -> tuple[str, list[Task]]:
    title, tasks = load_tasks(paths)
    draft = _load(paths)
    if "project_title" in draft:
        title = str(draft["project_title"])
    result = [task for task in tasks if task.id not in set(draft.get("dropped", []))]
    for task_id, fields in (draft.get("edits") or {}).items():
        task = next((item for item in result if item.id == task_id), None)
        if task:
            for field, value in fields.items():
                setattr(task, field, value)
    result.extend(Task.from_dict(item) for item in draft.get("added", []))
    return title, result


def _commit(paths: WilyPaths) -> int:
    if not paths.init_draft.exists():
        _common.emit_error("no draft pending")
        return _common.EXIT_FAILURE
    title, tasks = _apply(paths)
    try:
        check_dependencies(tasks)
    except DependencyError as exc:
        _common.emit_error(f"dependency check failed: {exc}")
        return _common.EXIT_FAILURE
    save_tasks(paths, title, tasks)
    paths.init_draft.unlink()
    _common.emit_text(f"replan applied: {len(tasks)} task(s)")
    return _common.EXIT_OK


def _cancel(paths: WilyPaths) -> int:
    if paths.init_draft.exists():
        paths.init_draft.unlink()
    _common.emit_text("replan draft discarded")
    return _common.EXIT_OK
