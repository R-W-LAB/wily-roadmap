"""Manifest-only multi-repo workspace support for Wily v3."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .config import load_actors, load_tasks, repo_mode
from .models import Task, TaskStatus
from .paths import WilyPaths
from .scheduling import parallel_candidates, waiting_candidates

SCHEMA_VERSION = "wily-workspace-v1"
MANIFEST_NAMES = ("wily-workspace.yaml", ".wily-workspace.yaml")


class WorkspaceManifestError(Exception):
    """Raised when a workspace manifest is missing or invalid."""


@dataclass(frozen=True)
class WorkspaceRepo:
    id: str
    path: Path
    title: str | None = None
    group: str | None = None

    def to_dict(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "path": str(self.path),
        }
        if self.title:
            data["title"] = self.title
        if self.group:
            data["group"] = self.group
        return data


@dataclass(frozen=True)
class WorkspaceConfig:
    title: str
    repos: list[WorkspaceRepo]
    manifest_path: Path

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": SCHEMA_VERSION,
            "title": self.title,
            "manifest_path": str(self.manifest_path),
            "repos": [repo.to_dict() for repo in self.repos],
        }


def discover_workspace_manifest(start: Path) -> Path:
    current = start.resolve()
    while True:
        for name in MANIFEST_NAMES:
            candidate = current / name
            if candidate.is_file():
                return candidate.resolve()
        if current.parent == current:
            raise WorkspaceManifestError(f"no wily-workspace.yaml or .wily-workspace.yaml at or above {start}")
        current = current.parent


def load_workspace(manifest_path: Path) -> WorkspaceConfig:
    manifest_path = manifest_path.resolve()
    data = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise WorkspaceManifestError(f"workspace manifest must be a mapping: {manifest_path}")
    schema = data.get("schema")
    if schema != SCHEMA_VERSION:
        raise WorkspaceManifestError(f"unsupported workspace manifest schema {schema!r}")
    repos_data = data.get("repos") or []
    if not isinstance(repos_data, list):
        raise WorkspaceManifestError("workspace manifest repos must be a list")
    base = manifest_path.parent
    repos = [_repo_from_dict(item, base=base, index=index) for index, item in enumerate(repos_data)]
    return WorkspaceConfig(
        title=str(data.get("title") or "Wily Workspace"),
        repos=repos,
        manifest_path=manifest_path,
    )


def workspace_snapshot(config: WorkspaceConfig) -> dict[str, object]:
    repos = [_repo_snapshot(repo) for repo in config.repos]
    return {
        "schema": SCHEMA_VERSION,
        "title": config.title,
        "manifest_path": str(config.manifest_path),
        "repos": repos,
    }


def workspace_next_tasks(config: WorkspaceConfig) -> list[dict[str, object]]:
    tasks: list[dict[str, object]] = []
    for repo in workspace_snapshot(config)["repos"]:
        if not isinstance(repo, dict) or repo.get("error"):
            continue
        tasks.extend(repo.get("next_tasks") or [])
    return tasks


def _repo_snapshot(repo: WorkspaceRepo) -> dict[str, object]:
    base: dict[str, object] = {
        "id": repo.id,
        "path": str(repo.path),
    }
    if repo.title:
        base["title"] = repo.title
    if repo.group:
        base["group"] = repo.group
    try:
        paths = _validated_repo_paths(repo)
        project_title, tasks = load_tasks(paths)
        actors = load_actors(paths)
        parallel = parallel_candidates(tasks)
        waiting = waiting_candidates(tasks)
        blocked = [task for task in tasks if task.status == TaskStatus.BLOCKED]
        in_progress = [task for task in tasks if task.status == TaskStatus.IN_PROGRESS]
        base.update(
            {
                "project_title": project_title,
                "mode": repo_mode(paths),
                "progress": _progress_payload(tasks, waiting=waiting),
                "in_progress_tasks": [_task_payload(task, repo=repo) for task in in_progress],
                "next_tasks": [_task_payload(task, repo=repo) for task in parallel],
                "waiting_tasks": [_task_payload(task, repo=repo) for task in waiting],
                "blocked_tasks": [_task_payload(task, repo=repo) for task in blocked],
                "actors": [{"id": actor.id, **actor.to_dict()} for actor in actors],
            }
        )
    except Exception as exc:
        base["error"] = str(exc)
    return base


def _validated_repo_paths(repo: WorkspaceRepo) -> WilyPaths:
    if not repo.path.is_dir():
        raise WorkspaceManifestError(f"repo path does not exist: {repo.path}")
    paths = WilyPaths(repo.path)
    if not paths.wily_dir.is_dir():
        raise WorkspaceManifestError(f"repo has no .wily/ directory: {repo.path}")
    if not paths.tasks_yaml.is_file():
        raise WorkspaceManifestError(f"repo has no .wily/tasks.yaml: {repo.path}")
    return paths


def _progress_payload(tasks: list[Task], *, waiting: list[Task]) -> dict[str, int]:
    total = len(tasks)
    done = sum(1 for task in tasks if task.status == TaskStatus.DONE)
    return {
        "total": total,
        "done": done,
        "in_progress": sum(1 for task in tasks if task.status == TaskStatus.IN_PROGRESS),
        "ready": sum(1 for task in tasks if task.status == TaskStatus.READY),
        "blocked": sum(1 for task in tasks if task.status == TaskStatus.BLOCKED),
        "waiting": len(waiting),
        "percent_done": int(round(done * 100 / total)) if total else 0,
    }


def _task_payload(task: Task, *, repo: WorkspaceRepo) -> dict[str, object]:
    data = task.to_dict()
    data["repo_id"] = repo.id
    data["repo_path"] = str(repo.path)
    if repo.group:
        data["repo_group"] = repo.group
    return data


def _repo_from_dict(item: Any, *, base: Path, index: int) -> WorkspaceRepo:
    if not isinstance(item, dict):
        raise WorkspaceManifestError(f"workspace repo entry {index + 1} must be a mapping")
    repo_id = str(item.get("id") or "").strip()
    path_value = str(item.get("path") or "").strip()
    if not repo_id:
        raise WorkspaceManifestError(f"workspace repo entry {index + 1} is missing id")
    if not path_value:
        raise WorkspaceManifestError(f"workspace repo {repo_id!r} is missing path")
    path = Path(path_value).expanduser()
    if not path.is_absolute():
        path = base / path
    return WorkspaceRepo(
        id=repo_id,
        path=path.resolve(),
        title=str(item["title"]) if item.get("title") else None,
        group=str(item["group"]) if item.get("group") else None,
    )
