"""`wily replan` - stage and commit task list edits."""

from __future__ import annotations

from pathlib import Path
import os
import stat
import subprocess
import sys
from typing import Any

import yaml

from ..config import load_actors, load_tasks, save_tasks, upsert_actor
from ..hooks.drift_guard import run_pre_commit_guard
from ..models import Actor, Task, TaskStatus
from ..paths import WilyPaths, WilyRootNotFound, find_wily_root, touch_wily
from ..transitions import DependencyError, check_dependencies
from . import _common

DESCRIPTION = "stage and commit task list edits"
USAGE = "usage: wily replan <show|add|revise-task|drop|assign|project|actor|commit|drift-guard|install-pre-commit-hook|cancel> [args]"
HELP = "\n".join(
    [
        "Subcommands:",
        "  show                         print current tasks and draft status",
        "  add <title>                  stage a new task",
        "  revise-task <id> <field> ... stage a task edit",
        "  drop <task-id>               stage task deletion",
        "  assign <task-id> <actor>     stage assignee change",
        "  actor add <id> [--email=...] add or update an actor",
        "  commit                       apply staged changes",
        "  cancel                       discard the draft",
    ]
)


def main(args: list[str]) -> int:
    args, as_json = _common.consume_json_flag(args)
    try:
        root = find_wily_root(Path.cwd())
    except WilyRootNotFound as exc:
        _common.emit_error(str(exc))
        return _common.EXIT_FAILURE
    paths = WilyPaths(root)
    if not args or args[0] == "show":
        return _show(paths, as_json=as_json)
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
    if sub == "actor":
        return _actor(paths, rest)
    if sub == "commit":
        return _commit(paths)
    if sub == "drift-guard":
        return _drift_guard(root, paths, rest)
    if sub == "install-pre-commit-hook":
        return _install_pre_commit_hook(root)
    if sub == "cancel":
        return _cancel(paths)
    _common.emit_error(f"unknown replan subcommand: {sub}")
    return _common.EXIT_USAGE


def _load(paths: WilyPaths) -> dict[str, Any]:
    if paths.replan_draft.exists():
        return yaml.safe_load(paths.replan_draft.read_text(encoding="utf-8")) or {}
    return {"mode": "replan", "added": [], "edits": {}, "dropped": []}


def _save(paths: WilyPaths, draft: dict[str, Any]) -> None:
    paths.init_dir.mkdir(parents=True, exist_ok=True)
    paths.replan_draft.write_text(
        yaml.safe_dump(draft, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    touch_wily(paths)


def _show(paths: WilyPaths, *, as_json: bool = False) -> int:
    title, tasks = load_tasks(paths)
    if as_json:
        _common.emit_json(
            {
                "project_title": title,
                "tasks": [task.to_dict() for task in tasks],
                "draft_pending": paths.replan_draft.exists(),
            }
        )
        return _common.EXIT_OK
    _common.emit_text(f"Project: {title}")
    for task in tasks:
        _common.emit_text(f"  {task.id} {task.status.value} {task.title}")
    if paths.replan_draft.exists():
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
    if task.status == TaskStatus.DONE:
        _common.emit_error(f"{task_id} is done; refusing to revise {field}")
        return _common.EXIT_TRANSITION
    if task.status == TaskStatus.IN_PROGRESS:
        _common.emit_error(f"warning: {task_id} is in_progress")
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


def _actor(paths: WilyPaths, args: list[str]) -> int:
    if len(args) < 2 or args[0] != "add":
        _common.emit_error("usage: wily replan actor add <id> [--email=<email>] [--name=<name>] [--display=<display>]")
        return _common.EXIT_USAGE
    actor_id = args[1]
    values = _flag_values(args[2:])
    existing = next((actor for actor in load_actors(paths) if actor.id == actor_id), None)
    emails = list(existing.git_author_emails) if existing else []
    names = list(existing.git_author_names) if existing else []
    if values.get("--email") and values["--email"] not in emails:
        emails.append(values["--email"])
    if values.get("--name") and values["--name"] not in names:
        names.append(values["--name"])
    display = values.get("--display") or (existing.display if existing else actor_id)
    upsert_actor(paths, Actor(id=actor_id, display=display, git_author_emails=emails, git_author_names=names, capacity=existing.capacity if existing else 1))
    _common.emit_text(f"actor added: {actor_id}")
    return _common.EXIT_OK


def _flag_values(args: list[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    index = 0
    while index < len(args):
        token = args[index]
        if token.startswith("--") and "=" in token:
            key, value = token.split("=", 1)
            values[key] = value
        elif token.startswith("--") and index + 1 < len(args):
            values[token] = args[index + 1]
            index += 1
        index += 1
    return values


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
    if not paths.replan_draft.exists():
        _common.emit_error("no draft pending")
        return _common.EXIT_FAILURE
    title, tasks = _apply(paths)
    try:
        check_dependencies(tasks)
    except DependencyError as exc:
        _common.emit_error(f"dependency check failed: {exc}")
        return _common.EXIT_FAILURE
    save_tasks(paths, title, tasks)
    paths.replan_draft.unlink()
    touch_wily(paths)
    _common.emit_text(f"replan applied: {len(tasks)} task(s)")
    return _common.EXIT_OK


def _cancel(paths: WilyPaths) -> int:
    if paths.replan_draft.exists():
        paths.replan_draft.unlink()
        touch_wily(paths)
    _common.emit_text("replan draft discarded")
    return _common.EXIT_OK


def _drift_guard(root: Path, paths: WilyPaths, args: list[str]) -> int:
    if "--from-hook" not in args:
        _common.emit_error("usage: wily replan drift-guard --from-hook")
        return _common.EXIT_USAGE
    try:
        stub = run_pre_commit_guard(root, paths)
    except Exception as exc:
        _common.emit_error(f"wily drift guard skipped: {exc}")
        return _common.EXIT_OK
    if stub:
        _common.emit_text(f"drift guard: created {stub.id} {stub.title!r}")
    return _common.EXIT_OK


def _install_pre_commit_hook(root: Path) -> int:
    hook_path = _git_hook_path(root, "pre-commit")
    if hook_path is None:
        _common.emit_error("not a git repository")
        return _common.EXIT_FAILURE
    hook_path.parent.mkdir(parents=True, exist_ok=True)
    script = Path(__file__).resolve().parents[2] / "wily.py"
    marker = "# wily-roadmap drift guard"
    body = "\n".join(
        [
            "#!/bin/sh",
            marker,
            f"exec {sh_quote(sys.executable)} {sh_quote(str(script))} replan drift-guard --from-hook",
            "",
        ]
    )
    if hook_path.exists():
        existing = hook_path.read_text(encoding="utf-8", errors="replace")
        if existing.strip() and marker not in existing:
            backup = hook_path.with_name("pre-commit.wily-backup")
            os.replace(hook_path, backup)
            _common.emit_text(f"existing pre-commit hook moved to {backup}")
    hook_path.write_text(body, encoding="utf-8")
    hook_path.chmod(hook_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    _common.emit_text(f"pre-commit drift guard installed: {hook_path}")
    return _common.EXIT_OK


def _git_hook_path(root: Path, hook: str) -> Path | None:
    result = subprocess.run(
        ["git", "rev-parse", "--git-path", f"hooks/{hook}"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return None
    path = Path(result.stdout.strip())
    return path if path.is_absolute() else root / path


def sh_quote(value: str) -> str:
    return "'" + value.replace("'", "'\"'\"'") + "'"
