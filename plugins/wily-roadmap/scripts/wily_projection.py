#!/usr/bin/env python3
"""Build the shared Wily roadmap projection for status, watch, and Board emitters."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import wily_state_summary


Stage = dict[str, Any]
Phase = dict[str, Any]


def utc_now_z() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_roadmap(root: Path) -> dict[str, Any]:
    path = root / ".wily" / "roadmap.yaml"
    if not path.exists():
        return {}
    return wily_state_summary.parse_roadmap(wily_state_summary.read_text(path))


def load_live_items(root: Path) -> list[dict[str, Any]]:
    active = root / ".wily" / "local" / "live" / "active"
    if not active.exists():
        return []
    items: list[dict[str, Any]] = []
    for path in sorted(active.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(payload, dict):
            items.append(payload)
    return items


def checkpoint_overlay_for(
    live_items: list[dict[str, Any]],
    stage_id: str,
    phase_id: str,
) -> dict[str, Any]:
    for item in live_items:
        if str(item.get("stage_id") or "") != stage_id:
            continue
        item_phase = str(item.get("phase_id") or item.get("item_id") or "")
        if item_phase not in {phase_id, f"{stage_id}/{phase_id}"}:
            continue
        checkpoint = item.get("checkpoint")
        if not isinstance(checkpoint, dict):
            continue
        return {
            "source": str(checkpoint.get("source") or "custom-workflow"),
            "is_durable": False,
            "status_board": str(checkpoint.get("status_board") or ""),
            "state": str(checkpoint.get("state") or ""),
            "progress": checkpoint.get("progress") if isinstance(checkpoint.get("progress"), dict) else {},
            "current": checkpoint.get("current") if isinstance(checkpoint.get("current"), dict) else {},
            "next": checkpoint.get("next") if isinstance(checkpoint.get("next"), dict) else {},
            "rows": checkpoint.get("rows") if isinstance(checkpoint.get("rows"), list) else [],
            "current_action": str(checkpoint.get("current_action") or ""),
            "blocker": str(checkpoint.get("blocker") or ""),
            "verification": checkpoint.get("verification") if isinstance(checkpoint.get("verification"), dict) else {},
        }
    return {}


def stage_aggregate(phases: list[Phase]) -> dict[str, int]:
    total = len([phase for phase in phases if phase.get("status") != "superseded"])
    done = sum(1 for phase in phases if phase.get("status") == "done")
    percent = round(done * 100 / total) if total else 0
    return {"done": done, "total": total, "percent": percent}


def phase_projection(stage: Stage, phase: Phase, live_items: list[dict[str, Any]]) -> dict[str, Any]:
    stage_id = str(stage.get("id") or stage.get("stage_id") or "")
    phase_id = str(phase.get("id") or "")
    return {
        "phase_id": phase_id,
        "ref": f"{stage_id}/{phase_id}",
        "title": str(phase.get("title") or "Untitled phase"),
        "status": str(phase.get("status") or "pending"),
        "runner": str(phase.get("runner") or "custom-workflow"),
        "depends_on": [str(value) for value in phase.get("depends_on") or []],
        "current_session": str(phase.get("current_session") or ""),
        "checkpoint_overlay": checkpoint_overlay_for(live_items, stage_id, phase_id),
    }


def stage_projection(stage: Stage, live_items: list[dict[str, Any]]) -> dict[str, Any]:
    phases = wily_state_summary.stage_child_phases(stage)
    return {
        "stage_id": str(stage.get("id") or stage.get("stage_id") or ""),
        "title": str(stage.get("title") or "Untitled stage"),
        "status": str(stage.get("status") or "pending"),
        "aggregate": stage_aggregate(phases),
        "depends_on": [str(value) for value in stage.get("depends_on") or []],
        "owner": str(stage.get("owner") or stage.get("assignee") or stage.get("assigned_to") or ""),
        "write_scope": [str(value) for value in stage.get("write_scope") or []],
        "phases": [phase_projection(stage, phase, live_items) for phase in phases],
    }


def build_projection(root: Path) -> dict[str, Any]:
    roadmap = load_roadmap(root)
    live_items = load_live_items(root)
    stages = wily_state_summary.enrich_stages_with_local_state(root, roadmap.get("stages") or [])
    warnings: list[str] = []
    if wily_state_summary.is_v2_roadmap(roadmap):
        stages = wily_state_summary.normalize_v2_stage_statuses(stages)
        for stage in stages:
            if stage.get("status") != "superseded" and not wily_state_summary.stage_child_phases(stage):
                warnings.append(f"Stage {stage.get('id')} has no child phases.")
    return {
        "schema": "wily-roadmap-projection-v1",
        "repo": root.name,
        "generated_at": utc_now_z(),
        "stages": [stage_projection(stage, live_items) for stage in stages],
        "live_overlays": live_items,
        "warnings": warnings,
    }
