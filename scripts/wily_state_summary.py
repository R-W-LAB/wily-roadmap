#!/usr/bin/env python3
"""Summarize Wily roadmap state for Codex."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any


Phase = dict[str, Any]


def repo_root(start: Path) -> Path:
    current = start.resolve()
    while True:
        if (current / ".git").exists():
            return current
        if current.parent == current:
            return start.resolve()
        current = current.parent


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def git_status(root: Path) -> str:
    if not (root / ".git").exists():
        return "not a git repo"

    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        return f"unavailable: {exc}"
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        return f"error: {detail}" if detail else "error"
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    return f"{len(lines)} changed file(s)"


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "null":
        return None
    if value == "[]":
        return []
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(part.strip()) for part in inner.split(",")]
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    if value.isdigit():
        return int(value)
    return value


def parse_key_value(line: str) -> tuple[str, Any] | None:
    if ":" not in line:
        return None
    key, value = line.split(":", 1)
    return key.strip(), parse_scalar(value.strip())


def parse_roadmap(content: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    phases: list[Phase] = []
    current_phase: Phase | None = None
    in_phases = False

    for raw_line in content.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue
        if line.strip().startswith("#"):
            continue

        if line == "phases:":
            in_phases = True
            data["phases"] = phases
            continue

        if not in_phases:
            parsed = parse_key_value(line)
            if parsed:
                key, value = parsed
                data[key] = value
            continue

        stripped = line.strip()
        if stripped.startswith("- "):
            current_phase = {}
            phases.append(current_phase)
            parsed = parse_key_value(stripped[2:])
            if parsed:
                key, value = parsed
                current_phase[key] = value
            continue

        if current_phase is not None:
            parsed = parse_key_value(stripped)
            if parsed:
                key, value = parsed
                current_phase[key] = value

    data.setdefault("phases", phases)
    return data


def phase_label(phase: Phase) -> str:
    return f"{phase.get('id', 'unknown')} {phase.get('title', 'Untitled phase')}"


def dependency_label(phase: Phase) -> str:
    depends_on = phase.get("depends_on") or []
    if not depends_on:
        return "depends on: none"
    return f"depends on: {', '.join(str(value) for value in depends_on)}"


def status_counts(phases: list[Phase]) -> dict[str, int]:
    statuses = ["done", "ready", "in_progress", "blocked", "superseded"]
    return {status: sum(1 for phase in phases if phase.get("status") == status) for status in statuses}


def phases_with_status(phases: list[Phase], status: str) -> list[Phase]:
    return [phase for phase in phases if phase.get("status") == status]


def summarize_roadmap(root: Path, state_dir: Path, roadmap: dict[str, Any]) -> str:
    phases = roadmap.get("phases") or []
    counts = status_counts(phases)
    ready = phases_with_status(phases, "ready")
    blocked = phases_with_status(phases, "blocked")
    superseded = phases_with_status(phases, "superseded")
    replacements = [phase for phase in phases if phase.get("replaces")]
    next_phase = ready[0] if ready else None

    lines = [
        f"Repo: {root}",
        f"State: {state_dir.name}",
        f"Git: {git_status(root)}",
        f"Roadmap version: {roadmap.get('roadmap_version', 'unknown')}",
    ]

    goal = roadmap.get("goal")
    if goal:
        lines.append(f"Goal: {goal}")

    lines.append(
        "Progress: "
        f"{counts['done']} done, "
        f"{counts['ready']} ready, "
        f"{counts['in_progress']} in progress, "
        f"{counts['blocked']} blocked, "
        f"{counts['superseded']} superseded"
    )

    if next_phase:
        lines.append(f"Next: {next_phase.get('id')} - {next_phase.get('title', 'Untitled phase')}")
    else:
        lines.append("Next: none")

    lines.append("Ready phases:")
    if ready:
        lines.extend(f"  - {phase_label(phase)}" for phase in ready)
    else:
        lines.append("  none")

    lines.append("Blocked phases:")
    if blocked:
        lines.extend(f"  - {phase_label(phase)} ({dependency_label(phase)})" for phase in blocked)
    else:
        lines.append("  none")

    if replacements:
        lines.append("Replacements:")
        for phase in replacements:
            replaced = ", ".join(str(value) for value in phase.get("replaces") or [])
            lines.append(f"  - {phase.get('id')} replaces {replaced}")

    if superseded:
        lines.append("Superseded phases:")
        lines.extend(f"  - {phase_label(phase)}" for phase in superseded)

    return "\n".join(lines)


def summarize_state(root: Path, state_dir: Path) -> str:
    roadmap_path = state_dir / "roadmap.yaml"
    if not roadmap_path.exists():
        return "\n".join(
            [
                f"Repo: {root}",
                f"State: {state_dir.name}",
                f"Git: {git_status(root)}",
                "Roadmap: missing",
            ]
        )

    roadmap = parse_roadmap(read_text(roadmap_path))
    return summarize_roadmap(root, state_dir, roadmap)


def main() -> int:
    root = repo_root(Path.cwd())
    state_dir = root / ".wily"
    if state_dir.exists():
        print(summarize_state(root, state_dir))
        return 0

    print(f"Repo: {root}")
    print("State: none")
    print(f"Git: {git_status(root)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
