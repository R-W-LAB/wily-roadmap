#!/usr/bin/env python3
"""Local Wily roadmap helper."""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import wily_state_summary


Phase = dict[str, Any]


def state_dir(root: Path) -> Path:
    return root / ".wily"


def write_once(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def quote(value: str) -> str:
    escaped = value.replace('"', '\\"')
    return f'"{escaped}"'


def write_baseline_roadmap(path: Path, goal: str | None) -> None:
    goal_value = goal or "User goal needed"
    write_once(
        path,
        "\n".join(
            [
                "roadmap_version: 1",
                f"goal: {quote(goal_value)}",
                "phases: []",
                "",
            ]
        ),
    )


def command_init(root: Path, args: list[str]) -> int:
    goal = " ".join(args).strip() or None
    state = state_dir(root)
    for name in ("phases", "sessions", "revisions"):
        (state / name).mkdir(parents=True, exist_ok=True)

    write_once(
        state / "project.md",
        "\n".join(
            [
                "# Wily Project",
                "",
                f"Root: {root}",
                f"Goal: {goal or 'User goal needed'}",
                "",
                "Current Baseline:",
                "- Repository scan needed before phase generation.",
                "",
            ]
        ),
    )
    write_baseline_roadmap(state / "roadmap.yaml", goal)
    write_once(
        state / "status.md",
        "\n".join(
            [
                "# Wily Status",
                "",
                "State initialized.",
                "Next action: scan the repository and generate roadmap phases.",
                "",
            ]
        ),
    )
    write_once(
        state / "decisions.md",
        "\n".join(
            [
                "# Wily Decisions",
                "",
                "No durable decisions recorded yet.",
                "",
            ]
        ),
    )

    print(f"Initialized .wily at {state}")
    if goal:
        print(f"Goal: {goal}")
    else:
        print("Goal: needed")
    return 0


def command_status(root: Path) -> int:
    state = state_dir(root)
    if state.exists():
        print(wily_state_summary.summarize_state(root, state))
        return 0
    print(f"Repo: {root}")
    print("State: none")
    print(f"Git: {wily_state_summary.git_status(root)}")
    return 0


def load_roadmap(root: Path) -> dict[str, Any]:
    path = state_dir(root) / "roadmap.yaml"
    if not path.exists():
        return {"roadmap_version": "unknown", "phases": []}
    return wily_state_summary.parse_roadmap(wily_state_summary.read_text(path))


def save_roadmap(root: Path, roadmap: dict[str, Any]) -> None:
    path = state_dir(root) / "roadmap.yaml"
    path.write_text(serialize_roadmap(roadmap), encoding="utf-8")


def find_phase(roadmap: dict[str, Any], phase_id: str) -> Phase | None:
    for phase in roadmap.get("phases") or []:
        if str(phase.get("id")) == phase_id:
            return phase
    return None


def ready_phase(roadmap: dict[str, Any]) -> Phase | None:
    for phase in roadmap.get("phases") or []:
        if phase.get("status") == "ready":
            return phase
    return None


def command_next(root: Path) -> int:
    roadmap = load_roadmap(root)
    phase = ready_phase(roadmap)
    if not phase:
        print("Next phase: none")
        return 0

    phase_id = phase.get("id", "unknown")
    title = phase.get("title", "Untitled phase")
    print(f"Next phase: {phase_id} - {title}")
    depends_on = phase.get("depends_on") or []
    print(f"Depends on: {', '.join(str(value) for value in depends_on) if depends_on else 'none'}")

    phase_path = phase.get("path")
    if not phase_path:
        print("Phase path: missing")
        return 0

    folder = state_dir(root) / str(phase_path)
    print(f"Phase path: {folder}")
    print()
    context, _planner = phase_context_bundle(str(phase_id), str(title), folder)
    print(context.strip())
    print("Approval required before implementation.")
    return 0


def serialize_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, list):
        return "[" + ", ".join(quote(str(item)) for item in value) + "]"
    if isinstance(value, int):
        return str(value)
    return quote(str(value))


def serialize_roadmap(roadmap: dict[str, Any]) -> str:
    lines: list[str] = []
    for key, value in roadmap.items():
        if key == "phases":
            continue
        lines.append(f"{key}: {serialize_scalar(value)}")

    phases = roadmap.get("phases") or []
    if not phases:
        lines.append("phases: []")
        return "\n".join(lines) + "\n"

    lines.append("phases:")
    for phase in phases:
        first = True
        for key, value in phase.items():
            prefix = "  - " if first else "    "
            lines.append(f"{prefix}{key}: {serialize_scalar(value)}")
            first = False
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def phase_slug(phase_id: str) -> str:
    return phase_id.lower().replace("/", "-")


def session_glob(root: Path, phase_id: str) -> list[Path]:
    return sorted((state_dir(root) / "sessions").glob(f"*phase-{phase_slug(phase_id)}-attempt-*"))


def next_attempt(root: Path, phase_id: str) -> int:
    return len(session_glob(root, phase_id)) + 1


def session_status_text(
    phase_id: str,
    attempt: int,
    status: str,
    blocker: str | None = None,
    planner: str | None = None,
) -> str:
    lines = [
        f'phase: "{phase_id}"',
        f"attempt: {attempt}",
        f'status: "{status}"',
    ]
    if planner:
        lines.append(f"planner: {quote(planner)}")
    if blocker:
        lines.append(f"blocker: {quote(blocker)}")
    return "\n".join(lines) + "\n"


def markdown_section(title: str, content: str) -> str:
    body = content.strip() or "Missing."
    return f"## {title}\n\n{body}\n"


def planner_recommendation(planner_text: str) -> str | None:
    for line in planner_text.splitlines():
        stripped = line.strip()
        prefix = "Recommended planner:"
        if stripped.startswith(prefix):
            value = stripped[len(prefix) :].strip()
            return value or None
    return None


def phase_context_bundle(phase_id: str, title: str, folder: Path | None) -> tuple[str, str | None]:
    if folder is None:
        return (
            "\n".join(
                [
                    "# Wily Phase Context",
                    "",
                    f"Phase: {phase_id} - {title}",
                    "",
                    "Phase folder is missing.",
                    "",
                ]
            ),
            None,
        )

    phase_text = wily_state_summary.read_text(folder / "phase.md")
    planner_text = wily_state_summary.read_text(folder / "planner.md")
    prompt_text = wily_state_summary.read_text(folder / "prompt.md")
    verification_text = wily_state_summary.read_text(folder / "verification.md")
    handoff_text = wily_state_summary.read_text(folder / "handoff.md")
    plan_text = wily_state_summary.read_text(folder / "plan.md")
    planner = planner_recommendation(planner_text)

    if not plan_text.strip():
        plan_text = "\n".join(
            [
                "No implementation plan exists yet.",
                "Use the recommended planner to create one if this phase needs a detailed plan.",
            ]
        )

    content = "\n".join(
        [
            "# Wily Phase Context",
            "",
            f"Phase: {phase_id} - {title}",
            "",
            markdown_section("Phase", phase_text),
            markdown_section("Planner Adapter", planner_text),
            markdown_section("Prompt", prompt_text),
            markdown_section("Verification", verification_text),
            markdown_section("Handoff", handoff_text),
            markdown_section("Existing Implementation Plan", plan_text),
        ]
    )
    return content, planner


def create_session(root: Path, phase: Phase, attempt: int) -> Path:
    phase_id = str(phase.get("id", "unknown"))
    title = str(phase.get("title", "Untitled phase"))
    stamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    session = state_dir(root) / "sessions" / f"{stamp}-phase-{phase_slug(phase_id)}-attempt-{attempt}"
    session.mkdir(parents=True, exist_ok=False)

    phase_path = phase.get("path")
    phase_folder = state_dir(root) / str(phase_path) if phase_path else None
    input_text, planner = phase_context_bundle(phase_id, title, phase_folder)
    verification = wily_state_summary.read_text(phase_folder / "verification.md") if phase_folder else ""

    (session / "status.yaml").write_text(
        session_status_text(phase_id, attempt, "started", planner=planner),
        encoding="utf-8",
    )
    (session / "input.md").write_text(input_text, encoding="utf-8")
    (session / "result.md").write_text("# Result\n\nPending.\n", encoding="utf-8")
    (session / "verification.md").write_text(verification or "# Verification\n\nPending.\n", encoding="utf-8")
    (session / "changed-files.md").write_text("# Changed Files\n\nPending.\n", encoding="utf-8")
    return session


def relative_session_path(root: Path, session: Path) -> str:
    return session.relative_to(state_dir(root)).as_posix()


def current_session_path(root: Path, phase: Phase) -> Path | None:
    value = phase.get("current_session")
    if not value:
        return None
    return state_dir(root) / str(value)


def update_session_status(root: Path, phase: Phase, status: str, blocker: str | None = None) -> None:
    session = current_session_path(root, phase)
    if not session:
        return
    status_path = session / "status.yaml"
    attempt = 1
    name = session.name
    marker = "-attempt-"
    if marker in name:
        suffix = name.rsplit(marker, 1)[-1]
        if suffix.isdigit():
            attempt = int(suffix)
    planner = None
    if status_path.exists():
        for line in status_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("planner:"):
                planner = wily_state_summary.parse_scalar(line.split(":", 1)[1].strip())
                break
    status_path.write_text(
        session_status_text(str(phase.get("id", "unknown")), attempt, status, blocker, planner),
        encoding="utf-8",
    )


def require_phase_id(args: list[str], command: str) -> str | None:
    if args:
        return args[0]
    print(f"Usage: wily.py {command} <phase-id>", file=sys.stderr)
    return None


def command_start(root: Path, args: list[str], *, retry: bool = False) -> int:
    phase_id = require_phase_id(args, "retry" if retry else "start")
    if not phase_id:
        return 2
    roadmap = load_roadmap(root)
    phase = find_phase(roadmap, phase_id)
    if not phase:
        print(f"Phase not found: {phase_id}", file=sys.stderr)
        return 1

    attempt = next_attempt(root, phase_id)
    session = create_session(root, phase, attempt)
    phase["status"] = "in_progress"
    phase["current_session"] = relative_session_path(root, session)
    if "blocker" in phase:
        del phase["blocker"]
    save_roadmap(root, roadmap)

    if retry:
        print(f"Started phase {phase_id} attempt {attempt}")
    else:
        print(f"Started phase {phase_id}")
    print(f"Session: {session}")
    return 0


def command_complete(root: Path, args: list[str]) -> int:
    phase_id = require_phase_id(args, "complete")
    if not phase_id:
        return 2
    roadmap = load_roadmap(root)
    phase = find_phase(roadmap, phase_id)
    if not phase:
        print(f"Phase not found: {phase_id}", file=sys.stderr)
        return 1
    phase["status"] = "done"
    update_session_status(root, phase, "verified")
    save_roadmap(root, roadmap)
    print(f"Completed phase {phase_id}")
    return 0


def command_block(root: Path, args: list[str]) -> int:
    phase_id = require_phase_id(args, "block")
    if not phase_id:
        return 2
    reason = " ".join(args[1:]).strip() or "Blocked without recorded reason"
    roadmap = load_roadmap(root)
    phase = find_phase(roadmap, phase_id)
    if not phase:
        print(f"Phase not found: {phase_id}", file=sys.stderr)
        return 1
    phase["status"] = "blocked"
    phase["blocker"] = reason
    update_session_status(root, phase, "blocked", reason)
    save_roadmap(root, roadmap)
    print(f"Blocked phase {phase_id}: {reason}")
    return 0


def command_replan(root: Path, args: list[str]) -> int:
    reason = " ".join(args).strip() or "Roadmap target changed"
    state = state_dir(root)
    revisions = state / "revisions"
    revisions.mkdir(parents=True, exist_ok=True)
    roadmap_path = state / "roadmap.yaml"
    roadmap = load_roadmap(root)
    current_version = roadmap.get("roadmap_version")
    version = current_version if isinstance(current_version, int) else 1
    roadmap["roadmap_version"] = version + 1
    roadmap_path.write_text(serialize_roadmap(roadmap), encoding="utf-8")

    stamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    revision_path = revisions / f"{stamp}-replan-{version}.md"
    completed = [phase for phase in roadmap.get("phases") or [] if phase.get("status") == "done"]
    revision_path.write_text(
        "\n".join(
            [
                f"# Roadmap Revision {version}",
                "",
                f"Reason: {reason}",
                "",
                "Completed phases kept:",
                *[f"- {phase.get('id')} {phase.get('title', 'Untitled phase')}" for phase in completed],
                *([] if completed else ["- none"]),
                "",
                "Next action:",
                "- Revise future phases from the current implementation baseline.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(f"Recorded replan revision: {revision_path}")
    print(f"Roadmap version: {version + 1}")
    return 0


def command_watch(root: Path) -> int:
    return command_status(root)


def usage() -> str:
    return "\n".join(
        [
            "Usage: wily.py <command> [args]",
            "",
            "Commands:",
            "  init [goal]",
            "  status",
            "  next",
            "  start <phase-id>",
            "  complete <phase-id>",
            "  block <phase-id> [reason]",
            "  retry <phase-id>",
            "  replan [reason]",
            "  watch",
        ]
    )


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    root = Path.cwd()
    if not argv:
        print(usage(), file=sys.stderr)
        return 2

    command, *args = argv
    if command == "init":
        return command_init(root, args)
    if command == "status":
        return command_status(root)
    if command == "next":
        return command_next(root)
    if command == "start":
        return command_start(root, args)
    if command == "complete":
        return command_complete(root, args)
    if command == "block":
        return command_block(root, args)
    if command == "retry":
        return command_start(root, args, retry=True)
    if command == "replan":
        return command_replan(root, args)
    if command == "watch":
        return command_watch(root)

    print(f"Unknown command: {command}", file=sys.stderr)
    print(usage(), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
