"""Board-backed task runtime helpers."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any

from .agent import client as agent_client
from .agent.config import AgentConfig, default_paths, load_config
from .config import save_tasks
from .models import Task, TaskStatus
from .paths import WilyPaths
from .progress import CpEvent, CpSummary, read_events


def load_board_config() -> AgentConfig:
    return load_config(default_paths().config_path)


def authority_enabled(config: AgentConfig) -> bool:
    return bool(config.task_authority)


def transition_task(
    config: AgentConfig,
    project_id: str,
    task_id: str,
    action: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    return agent_client.transition_task(config, project_id, task_id, action, payload)


def list_project_tasks(config: AgentConfig, project_id: str) -> dict[str, Any]:
    return agent_client.list_project_tasks(config, project_id)


def board_failure_message(result: dict[str, Any]) -> str:
    reason = str(result.get("reason") or result.get("detail") or "unknown error")
    status = result.get("status")
    suffix = f" (HTTP {status})" if status else ""
    return f"Board task authority failed{suffix}: {reason}"


def apply_runtime_response(task: Task, response: dict[str, Any]) -> Task:
    status = _task_status(response.get("status"), fallback=task.status)
    actor = _optional_str(response.get("actor"))
    owner = _optional_str(response.get("owner"))
    return replace(
        task,
        status=status,
        assignee=owner,
        actor=actor,
        claim_sha=_optional_str(response.get("claim_sha")),
        claim_at=_optional_str(response.get("claim_at")),
        done_at=_optional_str(response.get("done_at")),
        blocker=_optional_str(response.get("blocker")),
    )


def refresh_tasks_from_board(paths: WilyPaths, project_title: str, tasks: list[Task], config: AgentConfig) -> tuple[bool, str]:
    result = list_project_tasks(config, config.repo)
    if result.get("sent") is False:
        return False, board_failure_message(result)
    runtimes = {
        str(item.get("task_id")): item
        for item in result.get("tasks", [])
        if isinstance(item, dict) and item.get("task_id")
    }
    if not runtimes:
        return True, ""
    refreshed = [apply_runtime_response(task, runtimes[task.id]) if task.id in runtimes else task for task in tasks]
    save_tasks(paths, project_title, refreshed)
    return True, ""


def cp_payload_after_event(paths: WilyPaths, task_id: str, event: CpEvent) -> dict[str, Any]:
    return cp_payload_from_events([*read_events(paths, task_id), event], event)


def cp_payload_from_events(events: list[CpEvent], event: CpEvent) -> dict[str, Any]:
    summary = summarize_events(events)
    status = "done" if event.event == "done" else "running"
    if event.event == "cancel":
        status = "blocked"
    return {
        "cp_id": event.cp,
        "event": event.event,
        "status": status,
        "note": event.note,
        "done": summary.done,
        "total": summary.total,
        "current_cp": summary.current_cp,
        "cp_names": summary.cp_names,
        "done_cp_names": summary.done_cp_names,
        "at": event.ts,
    }


def summarize_events(events: list[CpEvent]) -> CpSummary:
    started: dict[str, bool] = {}
    done: dict[str, bool] = {}
    cp_order: list[str] = []
    last_event_at = None
    for event in events:
        last_event_at = event.ts
        if event.event == "start":
            started.setdefault(event.cp, True)
            if event.cp not in cp_order:
                cp_order.append(event.cp)
        elif event.event in {"done", "cancel"}:
            started.setdefault(event.cp, True)
            if event.cp not in cp_order:
                cp_order.append(event.cp)
            done[event.cp] = True
    active = set(started) - set(done)
    current = None
    for event in reversed(events):
        if event.event == "start" and event.cp in active:
            current = event.cp
            break
    return CpSummary(
        total=len(started),
        done=len(done),
        in_progress=len(active),
        current_cp=current,
        cp_names=cp_order,
        done_cp_names=[cp for cp in cp_order if cp in done],
        last_event_at=last_event_at,
    )


def config_error(config: AgentConfig) -> str | None:
    if not config.task_authority:
        return None
    missing = []
    if not config.board_url:
        missing.append("board_url")
    if not config.repo:
        missing.append("repo")
    if not config.token:
        missing.append("token")
    if missing:
        return "Board task authority is enabled but missing " + ", ".join(missing)
    return None


def project_config_for_root(_root: Path) -> AgentConfig:
    return load_board_config()


def _task_status(value: Any, *, fallback: TaskStatus) -> TaskStatus:
    try:
        return TaskStatus(str(value))
    except ValueError:
        return fallback


def _optional_str(value: Any) -> str | None:
    return str(value) if value not in {None, ""} else None
