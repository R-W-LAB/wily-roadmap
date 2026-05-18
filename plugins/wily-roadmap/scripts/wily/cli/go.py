"""`wily go <id>` - emit custom-workflow goal text."""

from __future__ import annotations

from pathlib import Path

from ..config import load_tasks
from ..models import Task, TaskStatus
from ..paths import WilyPaths, WilyRootNotFound, find_wily_root
from . import _common


def main(args: list[str]) -> int:
    as_json = "--json" in args
    positional = [arg for arg in args if not arg.startswith("--")]
    if len(positional) != 1:
        _common.emit_error("usage: wily go <task-id> [--json]")
        return _common.EXIT_USAGE
    task_id = positional[0]
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
    if task.status != TaskStatus.IN_PROGRESS:
        _common.emit_error(f"{task_id} is {task.status.value}; claim it first")
        return _common.EXIT_TRANSITION
    text = goal_text(root, paths, task)
    if as_json:
        _common.emit_json(
            {"task_id": task.id, "goal_text": text, "progress_jsonl": str(paths.progress_jsonl(task.id).relative_to(root))}
        )
    else:
        _common.emit_text(
            "==== copy below into custom-workflow-skillset:plan-goal-runner ====\n"
            + text
            + "===================================================================="
        )
    return _common.EXIT_OK


def goal_text(root: Path, paths: WilyPaths, task: Task) -> str:
    acceptance = task.acceptance
    if not acceptance and task.acceptance_file:
        candidate = root / task.acceptance_file
        if candidate.exists():
            acceptance = candidate.read_text(encoding="utf-8")
    scope = "\n".join(f"- {item}" for item in task.scope) or "(no scope declared)"
    progress = paths.progress_jsonl(task.id).relative_to(root)
    return (
        f"# Wily Task {task.id}: {task.title}\n\n"
        f"## Intent\n{task.intent or '(no intent)'}\n\n"
        f"## Acceptance\n{acceptance or '(no acceptance)'}\n\n"
        f"## Scope (allowed change paths)\n{scope}\n\n"
        f"## Progress recording\n"
        f"- {progress} is the Wily checkpoint ledger used by `wily watch`.\n"
        f"- When a custom-workflow checkpoint starts: `python3 plugins/wily-roadmap/scripts/wily.py cp {task.id} start <cp-name>`\n"
        f"- When that checkpoint passes verification: `python3 plugins/wily-roadmap/scripts/wily.py cp {task.id} done <cp-name>`\n"
        f"- To backfill from a custom-workflow status board: `python3 plugins/wily-roadmap/scripts/wily.py cp {task.id} import-status agent-handoffs/<slug>-status.md`\n"
        f"- commit trailer: Wily-Task: {task.id}, Wily-CP: <cp-name>\n\n"
        f"## After custom-workflow finishes\n"
        f"- Compare result against every acceptance item.\n"
        f"- Report any file outside Scope before closing.\n"
        f"- Use `wily done {task.id}` only after verification.\n"
    )
