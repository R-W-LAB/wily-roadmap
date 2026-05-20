"""Per-task `progress.jsonl` helpers."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Literal

from .paths import WilyPaths

EventKind = Literal["start", "done", "note", "ac", "cancel"]


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
class AcCheck:
    ts: str
    actor: str
    index: int
    status: str
    evidence: str = ""

    def to_event(self) -> CpEvent:
        note = json.dumps({"index": self.index, "status": self.status, "evidence": self.evidence}, ensure_ascii=False)
        return CpEvent(ts=self.ts, actor=self.actor, cp=f"AC{self.index}", event="ac", note=note)


@dataclass
class CpSummary:
    total: int
    done: int
    in_progress: int
    current_cp: str | None
    cp_names: list[str] = field(default_factory=list)
    done_cp_names: list[str] = field(default_factory=list)
    last_event_at: str | None = None


def init_progress(paths: WilyPaths, task_id: str) -> None:
    target = paths.progress_jsonl(task_id)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.touch(exist_ok=True)


def append_event(paths: WilyPaths, task_id: str, event: CpEvent) -> None:
    target = paths.progress_jsonl(task_id)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as fh:
        fh.write(event.to_json() + "\n")


def append_event_once(paths: WilyPaths, task_id: str, event: CpEvent) -> bool:
    for existing in read_events(paths, task_id):
        if existing.cp == event.cp and existing.event == event.event:
            return False
    append_event(paths, task_id, event)
    return True


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


def events_from_status_board(text: str, *, actor: str, ts: str) -> list[CpEvent]:
    events, _unrecognized = parse_status_board(text, actor=actor, ts=ts)
    return events


def parse_status_board(text: str, *, actor: str, ts: str) -> tuple[list[CpEvent], list[str]]:
    events: list[CpEvent] = []
    unrecognized: list[str] = []
    mode: str | None = None
    for line in text.splitlines():
        cells = _markdown_cells(line)
        if len(cells) < 2:
            mode = None
            if line.strip() and not line.lstrip().startswith("#"):
                unrecognized.append(line)
            continue
        detected = _status_table_mode(cells)
        if detected:
            mode = detected
            continue
        if set(cells[0]) <= {"-"} or set(cells[1]) <= {"-"}:
            continue
        if mode is None:
            continue
        checkpoint, status, evidence = _checkpoint_status_evidence(cells, mode=mode)
        if checkpoint.lower() in {"checkpoint", "ac", "acceptance", "acceptance criteria"}:
            continue
        if checkpoint.isdigit() and status.lower() in {"pass", "fail"}:
            events.append(AcCheck(ts=ts, actor=actor, index=int(checkpoint), status=status.lower(), evidence=evidence).to_event())
            continue
        if not checkpoint or not status:
            continue
        if status == "DONE":
            events.append(CpEvent(ts=ts, actor=actor, cp=checkpoint, event="start"))
            events.append(CpEvent(ts=ts, actor=actor, cp=checkpoint, event="done", note=evidence or None))
        elif status in {"RUNNING", "VERIFYING", "PARTIAL", "BLOCKED"}:
            events.append(CpEvent(ts=ts, actor=actor, cp=checkpoint, event="start"))
            if status == "BLOCKED":
                events.append(CpEvent(ts=ts, actor=actor, cp=checkpoint, event="cancel", note=evidence or None))
        else:
            unrecognized.append(line)
    return events, unrecognized


def read_ac_checks(paths: WilyPaths, task_id: str) -> list[AcCheck]:
    checks: list[AcCheck] = []
    for event in read_events(paths, task_id):
        if event.event != "ac" or not event.note:
            continue
        try:
            data = json.loads(event.note)
            checks.append(
                AcCheck(
                    ts=event.ts,
                    actor=event.actor,
                    index=int(data["index"]),
                    status=str(data["status"]),
                    evidence=str(data.get("evidence") or ""),
                )
            )
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            continue
    return sorted(checks, key=lambda item: item.index)


def _markdown_cells(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []
    return [cell.strip().strip("`") for cell in stripped.strip("|").split("|")]


def _status_table_mode(cells: list[str]) -> str | None:
    lowered = [cell.lower() for cell in cells]
    if len(lowered) >= 3 and lowered[0] == "id" and lowered[1] == "status" and lowered[2] == "checkpoint":
        return "custom-workflow"
    if len(lowered) >= 2 and lowered[0] in {"checkpoint", "cp"} and lowered[1] in {"status", "state"}:
        return "checkpoint"
    if len(lowered) >= 2 and lowered[0] in {"ac", "acceptance", "acceptance criteria"} and lowered[1] == "status":
        return "acceptance"
    return None


def _checkpoint_status_evidence(cells: list[str], *, mode: str) -> tuple[str, str, str]:
    if mode == "custom-workflow" and len(cells) >= 3:
        status = cells[1].upper()
        if status in {"DONE", "RUNNING", "VERIFYING", "PARTIAL", "BLOCKED", "TODO", "PENDING"}:
            evidence = cells[4] if len(cells) > 4 else ""
            return cells[2], status, evidence
    checkpoint, status = cells[0], cells[1].upper()
    evidence = cells[2] if len(cells) > 2 else ""
    return checkpoint, status, evidence


def cp_summary(paths: WilyPaths, task_id: str) -> CpSummary:
    events = read_events(paths, task_id)
    started: dict[str, bool] = {}
    done: dict[str, bool] = {}
    cp_order: list[str] = []
    for event in events:
        if event.event == "start":
            started.setdefault(event.cp, True)
            if event.cp not in cp_order:
                cp_order.append(event.cp)
        elif event.event == "done":
            done[event.cp] = True
        elif event.event == "cancel":
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
        last_event_at=events[-1].ts if events else None,
    )
