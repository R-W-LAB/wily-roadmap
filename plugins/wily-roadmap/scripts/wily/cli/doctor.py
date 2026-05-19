"""`wily doctor` - check local Wily project health."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import yaml

from ..config import SCHEMA_VERSION, load_actors, load_tasks
from ..models import TaskStatus
from ..paths import WilyPaths, WilyRootNotFound, find_wily_root
from . import _common

DESCRIPTION = "check local Wily project health"
USAGE = "usage: wily doctor [--fix] [--json]"
HELP = "\n".join(
    [
        "Options:",
        "  --fix   apply safe repairs such as creating missing progress ledgers",
        "  --json  emit diagnostics as JSON",
    ]
)


@dataclass(frozen=True)
class Diagnostic:
    level: Literal["ok", "warn", "fail"]
    code: str
    message: str
    fixed: bool = False


def main(args: list[str]) -> int:
    args, as_json = _common.consume_json_flag(args)
    fix = "--fix" in args
    try:
        root = find_wily_root(Path.cwd())
    except WilyRootNotFound as exc:
        _common.emit_error(str(exc))
        return _common.EXIT_FAILURE
    paths = WilyPaths(root)
    diagnostics = run_checks(root, paths, fix=fix)
    if as_json:
        _common.emit_json({"diagnostics": [item.__dict__ for item in diagnostics]})
    else:
        for item in diagnostics:
            line = f"{item.level}: {item.code}: {item.message}"
            if item.fixed:
                line += " (fixed)"
            (_common.emit_error if item.level in {"fail", "warn"} else _common.emit_text)(line)
    if any(item.level == "fail" and not item.fixed for item in diagnostics):
        return 2
    if any(item.level == "warn" for item in diagnostics):
        return 1
    return 0


def run_checks(root: Path, paths: WilyPaths, *, fix: bool = False) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    diagnostics.extend(_schema_checks(paths))
    try:
        _, tasks = load_tasks(paths)
        actors = load_actors(paths)
    except Exception as exc:
        return [*diagnostics, Diagnostic("fail", "state-load", f"cannot load Wily state: {exc}")]
    task_ids = {task.id for task in tasks}
    actor_ids = {actor.id for actor in actors}
    for task in tasks:
        for dependency in task.depends_on:
            if dependency not in task_ids:
                diagnostics.append(Diagnostic("fail", "broken-depends-on", f"{task.id} has broken depends_on {dependency}"))
        if task.status == TaskStatus.IN_PROGRESS and not paths.progress_jsonl(task.id).exists():
            fixed = False
            if fix:
                paths.progress_jsonl(task.id).parent.mkdir(parents=True, exist_ok=True)
                paths.progress_jsonl(task.id).touch()
                fixed = True
            diagnostics.append(Diagnostic("fail", "missing-progress", f"{task.id} missing progress.jsonl", fixed=fixed))
        if task.claim_sha and task.actor and task.actor not in actor_ids:
            diagnostics.append(Diagnostic("fail", "missing-actor", f"{task.id} references missing actor {task.actor}"))
    if paths.tasks_dir.exists():
        for task_dir in sorted(path for path in paths.tasks_dir.iterdir() if path.is_dir()):
            if task_dir.name not in task_ids:
                diagnostics.append(Diagnostic("warn", "orphan-task-dir", f"orphan task dir {task_dir.relative_to(root)}"))
    diagnostics.append(_hook_check(root))
    diagnostics.append(_venv_check(root))
    if not diagnostics:
        diagnostics.append(Diagnostic("ok", "state", "no issues found"))
    return diagnostics


def _schema_checks(paths: WilyPaths) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for path in (paths.tasks_yaml, paths.actors_yaml):
        if not path.exists():
            continue
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except Exception as exc:
            diagnostics.append(Diagnostic("fail", "schema", f"cannot parse {path.name}: {exc}"))
            continue
        schema = data.get("schema")
        if schema and schema != SCHEMA_VERSION:
            diagnostics.append(Diagnostic("fail", "schema", f"{path.name} schema {schema!r} is not {SCHEMA_VERSION!r}"))
    return diagnostics


def _hook_check(root: Path) -> Diagnostic:
    hook = root / ".git" / "hooks" / "pre-commit"
    try:
        text = hook.read_text(encoding="utf-8")
    except OSError:
        return Diagnostic("warn", "pre-commit-hook", "pre-commit hook is not installed")
    if "drift-guard --from-hook" not in text:
        return Diagnostic("warn", "pre-commit-hook", "pre-commit hook does not run wily drift guard")
    return Diagnostic("ok", "pre-commit-hook", "pre-commit hook runs wily drift guard")


def _venv_check(root: Path) -> Diagnostic:
    if (root / ".venv").exists() or (root / "venv").exists():
        return Diagnostic("ok", "venv", "virtual environment present")
    return Diagnostic("warn", "venv", "virtual environment not found")
