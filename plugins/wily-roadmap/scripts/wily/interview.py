"""Draft state for `wily init` interviews."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import yaml

from .paths import WilyPaths


@dataclass
class Draft:
    mode: str
    answers: dict[str, str] = field(default_factory=dict)
    history: list[str] = field(default_factory=list)
    task_candidates: list[dict[str, Any]] = field(default_factory=list)
    project_title: str = ""


def load_or_init_draft(paths: WilyPaths, *, mode: str) -> Draft:
    if not paths.init_draft.exists():
        return Draft(mode=mode)
    data = yaml.safe_load(paths.init_draft.read_text(encoding="utf-8")) or {}
    return Draft(
        mode=data.get("mode", mode),
        answers=dict(data.get("answers") or {}),
        history=list(data.get("history") or []),
        task_candidates=list(data.get("task_candidates") or []),
        project_title=str(data.get("project_title") or ""),
    )


def save_draft(paths: WilyPaths, draft: Draft) -> None:
    paths.init_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "mode": draft.mode,
        "answers": draft.answers,
        "history": draft.history,
        "task_candidates": draft.task_candidates,
        "project_title": draft.project_title,
    }
    paths.init_draft.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def discard_draft(paths: WilyPaths) -> None:
    if paths.init_draft.exists():
        paths.init_draft.unlink()


def record_answer(draft: Draft, *, key: str, text: str) -> None:
    draft.answers[key] = text
    if key in draft.history:
        draft.history.remove(key)
    draft.history.append(key)


def revise_answer(draft: Draft, *, key: str, text: str) -> None:
    if key not in draft.answers:
        raise KeyError(key)
    draft.answers[key] = text


def pop_last_answer(draft: Draft) -> str | None:
    if not draft.history:
        return None
    key = draft.history.pop()
    draft.answers.pop(key, None)
    return key


def add_task_candidate(draft: Draft, *, title: str) -> str:
    numbers = [
        int(item["id"][1:])
        for item in draft.task_candidates
        if str(item.get("id", "")).startswith("T") and str(item["id"])[1:].isdigit()
    ]
    task_id = f"T{(max(numbers) + 1) if numbers else 1:02d}"
    draft.task_candidates.append(
        {
            "id": task_id,
            "title": title,
            "intent": "",
            "acceptance": "",
            "scope": [],
            "depends_on": [],
            "status": "ready",
            "assignee": None,
        }
    )
    return task_id


def revise_task_candidate(draft: Draft, task_id: str, field: str, value: Any) -> None:
    for candidate in draft.task_candidates:
        if candidate["id"] == task_id:
            candidate[field] = value
            return
    raise KeyError(task_id)


def drop_task_candidate(draft: Draft, task_id: str) -> None:
    draft.task_candidates = [item for item in draft.task_candidates if item["id"] != task_id]


def assign_task_candidate(draft: Draft, task_id: str, actor: str) -> None:
    revise_task_candidate(draft, task_id, "assignee", actor)
