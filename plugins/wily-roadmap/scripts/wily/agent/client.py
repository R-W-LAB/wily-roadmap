"""Best-effort signed Wily Board event publisher."""

from __future__ import annotations

import hashlib
import hmac
import json
import urllib.error
import urllib.request
from typing import Any

from .config import AgentConfig


def sign_payload(secret: str, body: bytes) -> str:
    digest = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


def publish_event(config: AgentConfig, payload: dict[str, Any], timeout: float = 5.0) -> dict[str, Any]:
    if not config.configured:
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
