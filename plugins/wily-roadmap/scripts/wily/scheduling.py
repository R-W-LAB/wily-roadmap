"""Shared ready-task scheduling for `wily next` and `wily watch`."""

from __future__ import annotations

from .models import Task, TaskStatus


def dependencies_satisfied(task: Task, tasks: list[Task]) -> bool:
    done = {item.id for item in tasks if item.status == TaskStatus.DONE}
    return all(dep_id in done for dep_id in task.depends_on)


def parallel_candidates(tasks: list[Task], *, mine_actor_id: str | None = None) -> list[Task]:
    return sorted(
        [
            task
            for task in tasks
            if task.status == TaskStatus.READY
            and _matches_actor(task, mine_actor_id)
            and dependencies_satisfied(task, tasks)
        ],
        key=schedule_key,
    )


def waiting_candidates(tasks: list[Task], *, mine_actor_id: str | None = None) -> list[Task]:
    return sorted(
        [
            task
            for task in tasks
            if task.status == TaskStatus.READY
            and _matches_actor(task, mine_actor_id)
            and not dependencies_satisfied(task, tasks)
        ],
        key=schedule_key,
    )


def schedule_key(task: Task) -> tuple[int, str, int, str]:
    priority = task.priority if task.priority is not None else 999
    lane = task.parallel_lane or ""
    capacity = task.capacity_hint if task.capacity_hint is not None else 1
    return (priority, lane, capacity, task.id)


def _matches_actor(task: Task, mine_actor_id: str | None) -> bool:
    return not mine_actor_id or not task.assignee or task.assignee == mine_actor_id
