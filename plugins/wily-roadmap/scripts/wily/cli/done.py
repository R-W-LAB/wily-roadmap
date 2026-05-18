"""`wily done <id>` - mark a task done and write result.md."""

from __future__ import annotations

import fnmatch
from datetime import datetime, timezone
from pathlib import Path

from ..config import load_tasks, save_tasks
from ..observation import changed_files_since, head_sha
from ..paths import WilyPaths, WilyRootNotFound, find_wily_root
from ..progress import cp_summary
from ..transitions import TransitionError, apply_done
from . import _common


def main(args: list[str]) -> int:
    force = "--force" in args
    observed = "--observed" in args
    note = _extract_value(args, "--note")
    positional = _positionals(args, value_flags={"--note"})
    if len(positional) != 1:
        _common.emit_error("usage: wily done <task-id> [--note <text>] [--observed] [--force]")
        return _common.EXIT_USAGE
    task_id = positional[0]
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
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        updated = apply_done(task, at=now, force=force)
    except TransitionError as exc:
        _common.emit_error(str(exc))
        return _common.EXIT_TRANSITION
    current_sha = "?"
    changed: list[str] = []
    try:
        current_sha = head_sha(root)
        if task.claim_sha:
            changed = changed_files_since(root, task.claim_sha)
    except Exception:
        changed = []
    summary = cp_summary(paths, task_id)
    paths.task_dir(task_id).mkdir(parents=True, exist_ok=True)
    paths.result_md(task_id).write_text(
        _format_result(task, done_at=now, current_sha=current_sha, changed=changed, cp_total=summary.total, cp_done=summary.done, note=note, observed=observed),
        encoding="utf-8",
    )
    save_tasks(paths, project_title, [updated if item.id == task_id else item for item in tasks])
    _common.emit_text(f"{task_id}: {task.status.value} -> done")
    _common.emit_text(
        f"result.md written (changed {len(changed)} files, {summary.done}/{summary.total} cp, commit range {(task.claim_sha or '?')[:7]}..{current_sha[:7]})"
    )
    return _common.EXIT_OK


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


def _format_result(
    task,
    *,
    done_at: str,
    current_sha: str,
    changed: list[str],
    cp_total: int,
    cp_done: int,
    note: str | None,
    observed: bool,
) -> str:
    drift = _drift_summary(task.scope, changed)
    lines = [
        f"# {task.id}: {task.title} — done",
        "",
        f"- actor: {task.actor or '-'}{' (observed)' if observed else ''}",
        f"- claim: {task.claim_at or '-'} (sha {(task.claim_sha or '-')[:7]})",
        f"- done: {done_at}",
        f"- commit range: {(task.claim_sha or '?')[:7]}..{current_sha[:7]}",
        f"- changed files: {len(changed)}",
        f"- cp count: {cp_done}/{cp_total}",
        f"- scope drift: {drift}",
    ]
    if note:
        lines.append(f"- note: {note}")
    lines.append("")
    return "\n".join(lines)


def _drift_summary(scope: list[str], changed: list[str]) -> str:
    if not scope:
        return "(no scope declared)"
    outside = [file for file in changed if not any(fnmatch.fnmatch(file, pattern) for pattern in scope)]
    if not outside:
        return "0 files outside scope"
    return f"{len(outside)} files outside scope (first: {outside[0]})"
