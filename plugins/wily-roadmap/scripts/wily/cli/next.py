"""`wily next` - print the next ready task."""

from __future__ import annotations

from pathlib import Path

from ..config import load_actors, load_tasks
from ..models import Task, TaskStatus
from ..observation import git_config_identity, match_actor
from ..paths import WilyPaths, WilyRootNotFound, find_wily_root
from . import _common


def main(args: list[str]) -> int:
    mine = "--mine" in args
    as_json = "--json" in args
    try:
        root = find_wily_root(Path.cwd())
    except WilyRootNotFound as exc:
        _common.emit_error(str(exc))
        return _common.EXIT_FAILURE
    paths = WilyPaths(root)
    _, tasks = load_tasks(paths)
    actor_id = None
    if mine:
        email, name = git_config_identity(root)
        actor = match_actor(load_actors(paths), email=email, name=name)
        actor_id = actor.id if actor else None
    task = next_task(tasks, mine_actor_id=actor_id)
    if task is None:
        _common.emit_error("no ready task with satisfied dependencies")
        return _common.EXIT_FAILURE
    if as_json:
        _common.emit_json(task.to_dict())
    else:
        deps = ",".join(task.depends_on) if task.depends_on else "-"
        _common.emit_text(
            f"{task.id} ready  {task.title!r}  assignee={task.assignee or '-'}  depends_on=[{deps}] satisfied"
        )
    return _common.EXIT_OK


def next_task(tasks: list[Task], *, mine_actor_id: str | None = None) -> Task | None:
    done = {task.id for task in tasks if task.status == TaskStatus.DONE}
    for task in tasks:
        if task.status != TaskStatus.READY:
            continue
        if mine_actor_id and task.assignee and task.assignee != mine_actor_id:
            continue
        if all(dep in done for dep in task.depends_on):
            return task
    return None
