"""Foreground daemon loop for wily-agent."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from .client import publish_event
from .config import AgentConfig
from .registry import RegisteredRepo, load_registry
from .snapshot import heartbeat_payload, repo_snapshot


def run_once(config: AgentConfig, registry_path: Path, *, offline_ok: bool = False) -> list[dict[str, Any]]:
    repos = load_registry(registry_path)
    if not config.configured and offline_ok:
        return [{"repo": str(repo.path), "sent": False, "reason": "not configured"} for repo in repos]
    results: list[dict[str, Any]] = []
    for repo in repos:
        results.append(publish_repo_heartbeat(config, repo))
    return results


def run_loop(config: AgentConfig, registry_path: Path, *, once: bool = False, offline_ok: bool = False) -> list[dict[str, Any]]:
    results = run_once(config, registry_path, offline_ok=offline_ok)
    if once:
        return results
    while True:
        time.sleep(max(config.heartbeat_interval, 5))
        results = run_once(config, registry_path, offline_ok=offline_ok)


def publish_repo_heartbeat(config: AgentConfig, repo: RegisteredRepo) -> dict[str, Any]:
    try:
        snapshot = repo_snapshot(repo.path)
    except Exception as exc:  # best-effort daemon path
        return {"repo": str(repo.path), "sent": False, "reason": str(exc)}
    active = next((task for task in snapshot["tasks"] if task.get("status") == "in_progress"), None)
    task_id = str((active or snapshot["tasks"][0] if snapshot["tasks"] else {"id": "T00"}).get("id"))
    board_repo = repo.repo or config.repo
    payload = heartbeat_payload(
        repo=board_repo,
        actor=config.actor,
        task_id=task_id,
        note=f"{snapshot['project_title']} heartbeat",
    )
    result = publish_event(config, payload)
    return {"repo": str(repo.path), "task_id": task_id, **result}
