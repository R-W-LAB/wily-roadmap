"""Per-task `progress.jsonl` helpers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Literal

from .paths import WilyPaths

EventKind = Literal["start", "done", "note"]


@dataclass
class CpEvent:
    ts: str
    actor: str
    cp: str
    event: EventKind
    note: str | None = None

    def to_json(self) -> str:
        payload = {"ts": self.ts, "actor": self.actor, "cp": self.cp, "event": self.event}
        if self.note:
            payload["note"] = self.note
        return json.dumps(payload, ensure_ascii=False)

    @classmethod
    def from_json(cls, line: str) -> "CpEvent":
        data = json.loads(line)
        return cls(
            ts=data["ts"],
            actor=data["actor"],
            cp=data["cp"],
            event=data["event"],
            note=data.get("note"),
        )


@dataclass
class CpSummary:
    total: int
    done: int
    in_progress: int
    current_cp: str | None


def init_progress(paths: WilyPaths, task_id: str) -> None:
    target = paths.progress_jsonl(task_id)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.touch(exist_ok=True)


def append_event(paths: WilyPaths, task_id: str, event: CpEvent) -> None:
    target = paths.progress_jsonl(task_id)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as fh:
        fh.write(event.to_json() + "\n")


def read_events(paths: WilyPaths, task_id: str) -> list[CpEvent]:
    target = paths.progress_jsonl(task_id)
    if not target.exists():
        return []
    events: list[CpEvent] = []
    for line in target.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(CpEvent.from_json(line))
        except (json.JSONDecodeError, KeyError, TypeError):
            continue
    return events


def cp_summary(paths: WilyPaths, task_id: str) -> CpSummary:
    events = read_events(paths, task_id)
    started: dict[str, bool] = {}
    done: dict[str, bool] = {}
    for event in events:
        if event.event == "start":
            started.setdefault(event.cp, True)
        elif event.event == "done":
            done[event.cp] = True
    active = set(started) - set(done)
    current = None
    for event in reversed(events):
        if event.event == "start" and event.cp in active:
            current = event.cp
            break
    return CpSummary(total=len(started), done=len(done), in_progress=len(active), current_cp=current)
