"""`wily claim <id>` - transition a task into progress."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from ..config import load_actors, load_tasks, save_tasks
from ..observation import git_config_identity, head_sha, match_actor
from ..paths import WilyPaths, WilyRootNotFound, find_wily_root
from ..progress import init_progress
from ..transitions import TransitionError, apply_claim
from . import _common


def main(args: list[str]) -> int:
    force = "--force" in args
    positional = [arg for arg in args if not arg.startswith("--")]
    if len(positional) != 1:
        _common.emit_error("usage: wily claim <task-id> [--force]")
        return _common.EXIT_USAGE
    task_id = positional[0]
    try:
        root = find_wily_root(Path.cwd())
    except WilyRootNotFound as exc:
        _common.emit_error(str(exc))
        return _common.EXIT_FAILURE
    paths = WilyPaths(root)
    project_title, tasks = load_tasks(paths)
    email, name = git_config_identity(root)
    actor = match_actor(load_actors(paths), email=email, name=name)
    if actor is None:
        _common.emit_error("no actor matches current git author; update actors.yaml")
        return _common.EXIT_FAILURE
    task = next((item for item in tasks if item.id == task_id), None)
    if task is None:
        _common.emit_error(f"task not found: {task_id}")
        return _common.EXIT_FAILURE
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        updated = apply_claim(task, actor=actor.id, sha=head_sha(root), at=now, force=force)
    except TransitionError as exc:
        _common.emit_error(str(exc))
        return _common.EXIT_TRANSITION
    save_tasks(paths, project_title, [updated if item.id == task_id else item for item in tasks])
    init_progress(paths, task_id)
    if task.assignee and task.assignee != actor.id:
        _common.emit_text(f"warning: task assignee is {task.assignee}, actor is {actor.id}")
    _common.emit_text(f"{task_id}: {task.status.value} -> in_progress")
    _common.emit_text(f"actor: {actor.id} ({email or '-'})")
    _common.emit_text(f"claim_sha: {(updated.claim_sha or '')[:7]}")
    _common.emit_text(f"progress.jsonl initialized: {paths.progress_jsonl(task_id).relative_to(root)}")
    return _common.EXIT_OK
