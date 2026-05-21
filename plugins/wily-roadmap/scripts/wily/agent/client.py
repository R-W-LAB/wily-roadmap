"""Best-effort signed Wily Board event publisher."""

from __future__ import annotations

import hashlib
import hmac
import json
import urllib.error
import urllib.request
from typing import Any
from urllib.parse import quote

from .config import AgentConfig


def sign_payload(secret: str, body: bytes) -> str:
    digest = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


def publish_event(config: AgentConfig, payload: dict[str, Any], timeout: float = 5.0) -> dict[str, Any]:
    if not config.live_configured:
        return {"sent": False, "reason": "not configured"}
    url = config.board_url.rstrip("/") + "/api/live/events"
    body = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-Wily-Signature": sign_payload(config.secret, body),
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return {"sent": True, "status": response.status}
    except (OSError, urllib.error.HTTPError, urllib.error.URLError) as exc:
        return {"sent": False, "reason": str(exc)}


def register_agent(
    *,
    board_url: str,
    code: str,
    actor: str,
    machine_name: str,
    timeout: float = 5.0,
) -> dict[str, Any]:
    return post_json(
        board_url.rstrip("/") + "/agent/register",
        {"code": code, "actor": actor, "machine_name": machine_name},
        timeout=timeout,
    )


def publish_snapshot(config: AgentConfig, payload: dict[str, Any], timeout: float = 10.0) -> dict[str, Any]:
    if not config.snapshot_configured:
        return {"sent": False, "reason": "not logged in"}
    return sent_result(
        post_json(
            config.board_url.rstrip("/") + "/agent/snapshot",
            payload,
            token=config.token,
            timeout=timeout,
        )
    )


def publish_heartbeat(
    config: AgentConfig,
    *,
    project_id: str = "",
    current_task_id: str | None = None,
    payload: dict[str, Any] | None = None,
    timeout: float = 5.0,
) -> dict[str, Any]:
    if not config.snapshot_configured:
        return {"sent": False, "reason": "not logged in"}
    heartbeat = payload or {"project_id": project_id, "current_task_id": current_task_id, "actor": config.actor}
    return sent_result(
        post_json(
            config.board_url.rstrip("/") + "/agent/heartbeat",
            heartbeat,
            token=config.token,
            timeout=timeout,
        )
    )


def transition_task(
    config: AgentConfig,
    project_id: str,
    task_id: str,
    action: str,
    payload: dict[str, Any],
    timeout: float = 5.0,
) -> dict[str, Any]:
    if not config.task_authority_configured:
        return {"sent": False, "reason": "Board task authority is not configured"}
    return sent_result(
        post_json(
            _project_task_url(config, project_id, task_id, action),
            payload,
            token=config.token,
            timeout=timeout,
        )
    )


def list_project_tasks(config: AgentConfig, project_id: str, timeout: float = 5.0) -> dict[str, Any]:
    if not config.task_authority_configured:
        return {"sent": False, "reason": "Board task authority is not configured"}
    url = config.board_url.rstrip("/") + f"/agent/projects/{_project_path(project_id)}/tasks"
    return sent_result(get_json(url, token=config.token, timeout=timeout))


def sent_result(result: dict[str, Any]) -> dict[str, Any]:
    if result.get("sent") is False:
        return result
    return {"sent": True, **result}


def get_json(
    url: str,
    *,
    token: str = "",
    timeout: float = 5.0,
) -> dict[str, Any]:
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, method="GET", headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            response_body = response.read().decode("utf-8")
            data = json.loads(response_body) if response_body else {}
            return {"status": response.status, **data}
    except urllib.error.HTTPError as exc:
        return {"sent": False, "status": exc.code, "reason": exc.read().decode("utf-8", errors="replace") or str(exc)}
    except (OSError, urllib.error.URLError) as exc:
        return {"sent": False, "reason": str(exc)}


def post_json(
    url: str,
    payload: dict[str, Any],
    *,
    token: str = "",
    timeout: float = 5.0,
) -> dict[str, Any]:
    body = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, data=body, method="POST", headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            response_body = response.read().decode("utf-8")
            data = json.loads(response_body) if response_body else {}
            return {"status": response.status, **data}
    except urllib.error.HTTPError as exc:
        return {"sent": False, "status": exc.code, "reason": exc.read().decode("utf-8", errors="replace") or str(exc)}
    except (OSError, urllib.error.URLError) as exc:
        return {"sent": False, "reason": str(exc)}


def _project_task_url(config: AgentConfig, project_id: str, task_id: str, action: str) -> str:
    return config.board_url.rstrip("/") + f"/agent/projects/{_project_path(project_id)}/tasks/{quote(task_id, safe='')}/{action}"


def _project_path(project_id: str) -> str:
    owner, _, repo = project_id.partition("/")
    return f"{quote(owner, safe='')}/{quote(repo, safe='')}"
