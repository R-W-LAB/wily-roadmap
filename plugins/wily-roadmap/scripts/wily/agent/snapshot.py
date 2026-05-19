"""Snapshot helpers for registered Wily repositories."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from wily.config import load_tasks
from wily.paths import WilyPaths


def repo_snapshot(path: Path) -> dict[str, Any]:
    paths = WilyPaths(path)
    project_title, tasks = load_tasks(paths)
    return {
        "path": str(path),
        "project_title": project_title,
        "tasks": [task.to_dict() for task in tasks],
        "client_time": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }


def heartbeat_payload(*, repo: str, actor: str, task_id: str, note: str = "") -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return {
        "repo": repo,
        "item_type": "phase",
        "item_id": task_id,
        "phase_id": task_id,
        "actor": actor,
        "agent": "wily-agent",
        "event": "heartbeat",
        "live_status": "active",
        "session_id": f"wily-agent-{task_id}",
        "note": note,
        "client_time": now,
    }
