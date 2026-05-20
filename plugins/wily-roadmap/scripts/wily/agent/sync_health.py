"""Persist local wily-agent Board sync health."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_SYNC_HEALTH: dict[str, Any] = {
    "last_successful_push": "",
    "last_successful_snapshot": "",
    "last_successful_heartbeat": "",
    "last_failed_push": "",
    "last_failure_reason": "",
    "pending_snapshot_sha": "",
    "pending_snapshot_captured_at": "",
    "client_version": "",
    "captured_at": "",
}


def empty_sync_health() -> dict[str, Any]:
    return dict(DEFAULT_SYNC_HEALTH)


def load_sync_health(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return empty_sync_health()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return empty_sync_health()
    if not isinstance(data, dict):
        return empty_sync_health()
    health = empty_sync_health()
    health.update({key: value for key, value in data.items() if key in health})
    return health


def record_publish_result(
    path: Path,
    *,
    kind: str,
    snapshot_sha: str = "",
    result: dict[str, Any],
    client_version: str,
    captured_at: str,
) -> dict[str, Any]:
    health = load_sync_health(path)
    health["client_version"] = client_version
    health["captured_at"] = captured_at
    if result.get("sent") is True:
        health["last_successful_push"] = captured_at
        if kind == "snapshot":
            health["last_successful_snapshot"] = captured_at
            health["pending_snapshot_sha"] = ""
            health["pending_snapshot_captured_at"] = ""
            health["last_failure_reason"] = ""
        elif kind == "heartbeat":
            health["last_successful_heartbeat"] = captured_at
            if str(health.get("last_failure_reason") or "").startswith("heartbeat:"):
                health["last_failure_reason"] = ""
    else:
        reason = str(result.get("reason") or result.get("status") or "unknown")
        health["last_failed_push"] = captured_at
        health["last_failure_reason"] = f"{kind}: {reason}"
        if kind == "snapshot" and snapshot_sha:
            health["pending_snapshot_sha"] = snapshot_sha
            health["pending_snapshot_captured_at"] = captured_at
    write_sync_health(path, health)
    return health


def write_sync_health(path: Path, health: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_text(json.dumps(health, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)
