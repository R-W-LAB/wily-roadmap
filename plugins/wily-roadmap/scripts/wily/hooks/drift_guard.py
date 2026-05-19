"""Pre-commit drift guard helpers."""

from __future__ import annotations

import fnmatch
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from ..config import load_actors, load_tasks, save_tasks
from ..models import Task, TaskStatus
from ..observation import git_config_identity, head_sha, match_actor
from ..paths import WilyPaths


def staged_files(repo: Path) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


def run_pre_commit_guard(root: Path, paths: WilyPaths) -> Task | None:
    files = staged_files(root)
    if not files:
        return None
    project_title, tasks = load_tasks(paths)
    drift_files = files_requiring_stub(tasks, files)
    if not drift_files or _has_existing_drift_stub(tasks, drift_files):
        return None
    return ensure_drift_stub(root, paths, project_title, tasks, drift_files)


def ensure_drift_stub(root: Path, paths: WilyPaths, project_title: str, tasks: list[Task], files: list[str]) -> Task:
    existing = find_existing_drift_stub(tasks, files)
    if existing:
        return existing
    actor_id = _current_actor(root, paths)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    stub = Task(
        id=_next_id([task.id for task in tasks]),
        title=_stub_title(files),
        scope=list(files),
        status=TaskStatus.IN_PROGRESS,
        assignee=actor_id,
        actor=actor_id,
        claim_sha=_head_or_none(root),
        claim_at=now,
    )
    tasks.append(stub)
    save_tasks(paths, project_title, tasks)
    paths.progress_jsonl(stub.id).parent.mkdir(parents=True, exist_ok=True)
    paths.progress_jsonl(stub.id).touch(exist_ok=True)
    return stub


def files_requiring_stub(tasks: list[Task], changed_files: list[str]) -> list[str]:
    active = [task for task in tasks if task.status == TaskStatus.IN_PROGRESS and not task.title.startswith("drift:")]
    if not active:
        return list(changed_files)
    allowed: list[str] = []
    for task in active:
        allowed.extend(task.scope)
    if not allowed:
        return list(changed_files)
    return [file for file in changed_files if not any(fnmatch.fnmatch(file, pattern) for pattern in allowed)]


def _has_existing_drift_stub(tasks: list[Task], files: list[str]) -> bool:
    return find_existing_drift_stub(tasks, files) is not None


def find_existing_drift_stub(tasks: list[Task], files: list[str]) -> Task | None:
    target = set(files)
    for task in tasks:
        if task.status == TaskStatus.IN_PROGRESS and task.title.startswith("drift:") and target.issubset(set(task.scope)):
            return task
    return None


def _next_id(existing: list[str]) -> str:
    nums = [int(item[1:]) for item in existing if item.startswith("T") and item[1:].isdigit()]
    return f"T{(max(nums) + 1) if nums else 1:02d}"


def _stub_title(files: list[str]) -> str:
    if len(files) == 1:
        return f"drift: {files[0]}"
    return f"drift: {files[0]} (+{len(files) - 1} files)"


def _current_actor(root: Path, paths: WilyPaths) -> str | None:
    email, name = git_config_identity(root)
    actor = match_actor(load_actors(paths), email=email, name=name)
    return actor.id if actor else None


def _head_or_none(root: Path) -> str | None:
    try:
        return head_sha(root)
    except Exception:
        return None
