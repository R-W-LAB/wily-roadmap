"""Resolve `.wily/` roots and compose canonical v3 paths."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


class WilyRootNotFound(Exception):
    """Raised when no `.wily/` directory exists at or above a path."""


def find_wily_root(start: Path) -> Path:
    current = start.resolve()
    while True:
        if (current / ".wily").is_dir():
            return current
        if current.parent == current:
            raise WilyRootNotFound(f"no .wily/ directory at or above {start}")
        current = current.parent


@dataclass(frozen=True)
class WilyPaths:
    root: Path

    @property
    def wily_dir(self) -> Path:
        return self.root / ".wily"

    @property
    def tasks_yaml(self) -> Path:
        return self.wily_dir / "tasks.yaml"

    @property
    def actors_yaml(self) -> Path:
        return self.wily_dir / "actors.yaml"

    @property
    def project_md(self) -> Path:
        return self.wily_dir / "project.md"

    @property
    def tasks_dir(self) -> Path:
        return self.wily_dir / "tasks"

    def task_dir(self, task_id: str) -> Path:
        return self.tasks_dir / task_id

    def progress_jsonl(self, task_id: str) -> Path:
        return self.task_dir(task_id) / "progress.jsonl"

    def result_md(self, task_id: str) -> Path:
        return self.task_dir(task_id) / "result.md"

    def acceptance_md(self, task_id: str) -> Path:
        return self.task_dir(task_id) / "acceptance.md"

    @property
    def init_dir(self) -> Path:
        return self.wily_dir / "init"

    @property
    def init_draft(self) -> Path:
        return self.init_dir / "draft.yaml"

    @property
    def archive_dir(self) -> Path:
        return self.wily_dir / "archive"
