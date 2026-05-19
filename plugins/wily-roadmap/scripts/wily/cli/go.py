"""`wily go <id>` - emit custom-workflow goal text."""

from __future__ import annotations

from pathlib import Path

from ..config import load_tasks
from ..models import Task, TaskStatus
from ..paths import WilyPaths, WilyRootNotFound, find_wily_root
from . import _common

DESCRIPTION = "emit custom-workflow goal text"
USAGE = "usage: wily go <task-id> [--json]"
HELP = "\n".join(
    [
        "Options:",
        "  --json  emit task id, goal text, and progress ledger path as JSON",
    ]
)


def main(args: list[str]) -> int:
    args, as_json = _common.consume_json_flag(args)
    positional = _common.positionals(args)
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
    acceptance = task_acceptance(root, task)
    if not acceptance.strip():
        _common.emit_error(f"warning: {task.id} has empty acceptance; verify task criteria before implementation")
    text = goal_text(root, paths, task, acceptance=acceptance)
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


def task_acceptance(root: Path, task: Task) -> str:
    acceptance = task.acceptance_text
    if not acceptance and task.acceptance_file:
        candidate = root / task.acceptance_file
        if candidate.exists():
            acceptance = candidate.read_text(encoding="utf-8")
    return acceptance


def goal_text(root: Path, paths: WilyPaths, task: Task, *, acceptance: str | None = None) -> str:
    if acceptance is None:
        acceptance = task_acceptance(root, task)
    scope = "\n".join(f"- {item}" for item in task.scope) or "(no scope declared)"
    progress = paths.progress_jsonl(task.id).relative_to(root)
    return (
        f"# Wily Task {task.id}: {task.title}\n\n"
        f"## Intent\n{task.intent or '(no intent)'}\n\n"
        f"## Acceptance\n{acceptance or '(no acceptance)'}\n\n"
        f"## Scope (allowed change paths)\n{scope}\n\n"
        f"## Progress recording\n"
        f"- {progress} is the Wily checkpoint ledger used by `wily watch`.\n"
        f"- [ ] 1. Start checkpoint: `wily cp {task.id} start <cp-name>`.\n"
        f"- [ ] 2. Finish checkpoint after verification: `wily cp {task.id} done <cp-name>`.\n"
        f"- [ ] 3. Backfill if needed: `wily cp {task.id} import-status` "
        f"(default: `.wily/handoffs/{task.id}/status.md`).\n"
        f"- [ ] Before each checkpoint: run `wily cp {task.id} start <cp-name>`.\n"
        f"- [ ] After checkpoint verification passes: run `wily cp {task.id} done <cp-name>`.\n"
        f"- [ ] If a custom-workflow status board already exists: run `wily cp {task.id} import-status .wily/handoffs/{task.id}/status.md`.\n"
        f"- [ ] If commits are created, add trailers: Wily-Task: {task.id}, Wily-CP: <cp-name>.\n"
        f"- Custom Workflow interface contract: custom-workflow does not update Wily by itself; these `wily cp` calls bridge the cp automation gap.\n\n"
        f"## After custom-workflow finishes\n"
        f"- Compare result against every acceptance item.\n"
        f"- Report any file outside Scope before closing.\n"
        f"- Use `wily done {task.id}` only after verification.\n"
    )
