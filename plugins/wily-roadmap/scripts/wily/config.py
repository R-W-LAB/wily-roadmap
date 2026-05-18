"""Load and save Wily v3 state files."""

from __future__ import annotations

from typing import Iterable

import yaml

from .models import Actor, Task
from .paths import WilyPaths

SCHEMA_VERSION = "wily-v3"


def load_tasks(paths: WilyPaths) -> tuple[str, list[Task]]:
    if not paths.tasks_yaml.exists():
        return "", []
    data = yaml.safe_load(paths.tasks_yaml.read_text(encoding="utf-8")) or {}
    schema = data.get("schema")
    if schema and schema != SCHEMA_VERSION:
        raise ValueError(f"unsupported tasks.yaml schema {schema!r}")
    return str(data.get("project_title") or ""), [
        Task.from_dict(item) for item in data.get("tasks") or []
    ]


def save_tasks(paths: WilyPaths, project_title: str, tasks: Iterable[Task]) -> None:
    paths.wily_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": SCHEMA_VERSION,
        "project_title": project_title,
        "tasks": [task.to_dict() for task in tasks],
    }
    paths.tasks_yaml.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def load_actors(paths: WilyPaths) -> list[Actor]:
    if not paths.actors_yaml.exists():
        return []
    data = yaml.safe_load(paths.actors_yaml.read_text(encoding="utf-8")) or {}
    schema = data.get("schema")
    if schema and schema != SCHEMA_VERSION:
        raise ValueError(f"unsupported actors.yaml schema {schema!r}")
    actors = data.get("actors") or {}
    return [Actor.from_dict(actor_id, value or {}) for actor_id, value in actors.items()]


def save_actors(paths: WilyPaths, actors: Iterable[Actor]) -> None:
    paths.wily_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": SCHEMA_VERSION,
        "actors": {actor.id: actor.to_dict() for actor in actors},
    }
    paths.actors_yaml.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def repo_mode(paths: WilyPaths) -> str:
    return "collab" if len(load_actors(paths)) >= 2 else "solo"
