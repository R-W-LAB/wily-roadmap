#!/usr/bin/env python3
"""Prepare Wily phases for Custom Workflow Skillset execution."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import wily
import wily_state_summary


Phase = dict[str, Any]
ALLOWED_AUTONOMY_MODES = {"conservative", "goal_scoped", "yolo"}
CUSTOM_WORKFLOW_ENGINE = "custom-workflow-skillset"
CUSTOM_WORKFLOW_ALIASES = {"custom-workflow", "custom-workflow-skillset", "plan-goal-runner"}
PRIMARY_SKILL = "custom-workflow-skillset:plan-goal-runner"
PARALLEL_SKILL = "custom-workflow-skillset:parallel-lane-runner"


def parse_args(args: list[str]) -> tuple[str | None, str, str, bool, str | None]:
    phase_id: str | None = None
    workflow = "custom-workflow"
    autonomy_mode = "goal_scoped"
    dry_run = False
    error: str | None = None
    index = 0
    while index < len(args):
        arg = args[index]
        if arg == "--dry-run":
            dry_run = True
            index += 1
            continue
        if arg == "--runner":
            try:
                workflow = args[index + 1]
            except IndexError:
                error = "Missing value for --runner"
                break
            index += 2
            continue
        if arg == "--autonomy":
            try:
                autonomy_mode = args[index + 1]
            except IndexError:
                error = "Missing value for --autonomy"
                break
            index += 2
            continue
        if arg.startswith("--"):
            error = f"Unknown option: {arg}"
            break
        if phase_id is None:
            phase_id = arg
        else:
            error = f"Unexpected argument: {arg}"
            break
        index += 1
    return phase_id, workflow, autonomy_mode, dry_run, error


def workflow_engine(workflow: str) -> str:
    if workflow in CUSTOM_WORKFLOW_ALIASES:
        return CUSTOM_WORKFLOW_ENGINE
    return workflow


def validate_autonomy(autonomy_mode: str) -> str | None:
    if autonomy_mode not in ALLOWED_AUTONOMY_MODES:
        return f"Unsupported autonomy mode: {autonomy_mode}"
    return None


def phase_executable(phase: Phase, phases: list[Phase]) -> bool:
    status = str(phase.get("status") or "pending")
    if status in {"ready", "in_progress"}:
        return True
    return status == "pending" and wily_state_summary.dependencies_done(phase, phases)


def stage_phase_executable(root: Path, roadmap: dict[str, Any], stage: dict[str, Any], phase: Phase) -> bool:
    stages = wily_state_summary.enrich_stages_with_local_state(root, roadmap.get("stages") or [])
    stage_id = str(stage.get("id"))
    enriched_stage = next((candidate for candidate in stages if str(candidate.get("id")) == stage_id), stage)
    enriched_phase = next(
        (
            candidate
            for candidate in wily_state_summary.stage_child_phases(enriched_stage)
            if str(candidate.get("id")) == str(phase.get("id"))
        ),
        phase,
    )
    status = str(enriched_phase.get("status") or "pending")
    if status in {"ready", "in_progress"}:
        return True
    return status == "pending" and wily_state_summary.child_phase_dependencies_done(enriched_stage, enriched_phase, stages)


def ensure_session(root: Path, phase: Phase, roadmap: dict[str, Any]) -> Path:
    session = wily.current_session_path(root, phase)
    if str(phase.get("status")) == "in_progress" and session is not None and session.exists():
        return session

    phase_id = str(phase.get("id", "unknown"))
    attempt = wily.next_attempt(root, phase_id)
    session = wily.create_session(root, phase, attempt)
    phase["status"] = "in_progress"
    phase["current_session"] = wily.relative_session_path(root, session)
    phase.pop("blocker", None)
    wily.save_roadmap(root, roadmap)
    return session


def ensure_stage_phase_session(
    root: Path,
    roadmap: dict[str, Any],
    stage: dict[str, Any],
    phase: Phase,
    stage_state: dict[str, Any],
    phase_ref: str,
) -> Path:
    session = wily.current_session_path(root, phase)
    if str(phase.get("status")) == "in_progress" and session is not None and session.exists():
        return session

    attempt = wily.next_attempt(root, phase_ref)
    session = wily.create_session(root, {**phase, "id": phase_ref}, attempt)
    phase["status"] = "in_progress"
    phase["current_session"] = wily.relative_session_path(root, session)
    phase.pop("blocker", None)
    stage["status"] = "in_progress"
    stage["current_session"] = wily.relative_session_path(root, session)
    wily.save_stage_state(root, stage, stage_state)
    wily.save_roadmap(root, roadmap)
    return session


def slugify_phase(phase: Phase) -> str:
    phase_id = str(phase.get("id", "phase"))
    title = str(phase.get("title", "phase"))
    return f"{wily.phase_slug(phase_id)}-{wily.slugify_title(title)}"


def relative_to_root(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def native_goal_command(
    phase: Phase,
    engine: str,
    autonomy_mode: str,
    request_path: Path,
    result_path: Path,
    root: Path,
) -> str:
    phase_id = str(phase.get("id", "unknown"))
    title = str(phase.get("title", "Untitled phase"))
    request_ref = relative_to_root(root, request_path)
    result_ref = relative_to_root(root, result_path)
    skill = PRIMARY_SKILL if engine == CUSTOM_WORKFLOW_ENGINE else engine
    return (
        f"/goal Execute Wily phase {phase_id}: {title}. "
        f"Use {skill} with {autonomy_mode} autonomy. "
        f"Read {request_ref}. Write the execution result to {result_ref}. "
        "Do not mark the Wily phase done; finish with a recommended Wily status."
    )


def render_custom_workflow_request(
    phase: Phase,
    workflow: str,
    engine: str,
    autonomy_mode: str,
    session: Path,
    root: Path,
    result_path: Path,
) -> str:
    phase_id = str(phase.get("id", "unknown"))
    title = str(phase.get("title", "Untitled phase"))
    phase_folder = root / ".wily" / str(phase.get("path"))
    phase_context, _planner = wily.phase_context_bundle(phase_id, title, phase_folder)
    return "\n".join(
        [
            "# Wily Custom Workflow Skillset Request",
            "",
            f"- Phase ID: `{phase_id}`",
            f"- Phase title: `{title}`",
            f"- Workflow engine: `{engine}`",
            f"- Runner alias: `{workflow}`",
            f"- Autonomy mode: `{autonomy_mode}`",
            f"- Wily session: `{relative_to_root(root, session)}`",
            f"- Result target: `{relative_to_root(root, result_path)}`",
            f"- Git status: `{wily_state_summary.git_status(root)}`",
            "",
            "## Required Routing",
            "",
            f"- Use `{PRIMARY_SKILL}` as the execution engine for this phase.",
            f"- If that execution package returns `PARALLEL_SAFE` or `PARALLEL_SAFE_WITH_LIMITS`, use `{PARALLEL_SKILL}` for the approved bounded lanes.",
            "- Keep Wily as the roadmap owner. Custom Workflow owns the implementation execution package, progress, and verification evidence.",
            "",
            "## Result Contract",
            "",
            f"- Write the final execution result to `{relative_to_root(root, result_path)}`.",
            "- Include: final state, changed files, verification commands and outcomes, blockers if any, and recommended Wily status.",
            "- Recommended Wily status must be one of: `needs_review`, `blocked`, `ready`, or `done`.",
            "- Do not mark the Wily phase done directly.",
            "- After verification evidence exists, the active agent should run `$wily-complete <stage-id>/<phase-id>` or `$wily-block <stage-id>/<phase-id> \"<reason>\"`; use the legacy phase-only id only for non-v2 roadmaps.",
            "",
            "## Phase Context",
            "",
            phase_context.strip(),
            "",
        ]
    )


def result_template(phase: Phase, session: Path, root: Path) -> str:
    phase_id = str(phase.get("id", "unknown"))
    title = str(phase.get("title", "Untitled phase"))
    return "\n".join(
        [
            "# Custom Workflow Result",
            "",
            f"- Phase ID: `{phase_id}`",
            f"- Phase title: `{title}`",
            f"- Wily session: `{relative_to_root(root, session)}`",
            "",
            "## Final State",
            "",
            "Pending.",
            "",
            "## Changed Files",
            "",
            "Pending.",
            "",
            "## Verification",
            "",
            "Pending.",
            "",
            "## Recommended Wily Status",
            "",
            "Pending.",
            "",
        ]
    )


def text_is_pending(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return True
    metadata_prefixes = ("- Phase ID:", "- Phase title:", "- Wily session:")
    meaningful = [
        line.strip()
        for line in stripped.splitlines()
        if line.strip()
        and not line.startswith("#")
        and not line.strip().startswith(metadata_prefixes)
    ]
    return not meaningful or all(line in {"Pending.", "- Pending."} for line in meaningful)


def write_if_missing_or_pending(path: Path, text: str) -> None:
    if path.exists() and not text_is_pending(path.read_text(encoding="utf-8")):
        return
    path.write_text(text, encoding="utf-8")


def workflow_paths(root: Path, phase: Phase, session: Path) -> dict[str, Path]:
    slug = slugify_phase(phase)
    handoffs_dir = root / "agent-handoffs"
    return {
        "session_request": session / "custom-workflow-request.md",
        "session_result": session / "custom-workflow-result.md",
        "external_request": handoffs_dir / f"{slug}-custom-workflow-request.md",
        "external_result": handoffs_dir / f"{slug}-custom-workflow-result.md",
    }


def write_workflow_status(
    session: Path,
    engine: str,
    workflow: str,
    autonomy_mode: str,
    request_path: Path,
    result_path: Path,
    root: Path,
) -> None:
    status_path = session / "status.yaml"
    existing = status_path.read_text(encoding="utf-8") if status_path.exists() else ""
    filtered = [
        line
        for line in existing.splitlines()
        if not line.startswith(("workflow_engine:", "workflow_runner_alias:", "workflow_autonomy:", "workflow_request:", "workflow_result:"))
    ]
    filtered.extend(
        [
            f"workflow_engine: {wily.quote(engine)}",
            f"workflow_runner_alias: {wily.quote(workflow)}",
            f"workflow_autonomy: {wily.quote(autonomy_mode)}",
            f"workflow_request: {wily.quote(relative_to_root(root, request_path))}",
            f"workflow_result: {wily.quote(relative_to_root(root, result_path))}",
        ]
    )
    status_path.write_text("\n".join(filtered).rstrip() + "\n", encoding="utf-8")


def write_custom_workflow_request(
    root: Path,
    phase: Phase,
    workflow: str,
    engine: str,
    autonomy_mode: str,
    session: Path,
) -> dict[str, Path]:
    paths = workflow_paths(root, phase, session)
    paths["external_request"].parent.mkdir(parents=True, exist_ok=True)
    request_text = render_custom_workflow_request(
        phase,
        workflow,
        engine,
        autonomy_mode,
        session,
        root,
        paths["external_result"],
    )
    paths["external_request"].write_text(request_text, encoding="utf-8")
    paths["session_request"].write_text(request_text, encoding="utf-8")
    template = result_template(phase, session, root)
    write_if_missing_or_pending(paths["external_result"], template)
    write_if_missing_or_pending(paths["session_result"], template)
    write_workflow_status(
        session,
        engine,
        workflow,
        autonomy_mode,
        paths["external_request"],
        paths["external_result"],
        root,
    )
    return {"session": session, **paths}


def material_workflow_result(paths: list[Path]) -> str | None:
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if not text_is_pending(text):
            return text
    return None


def write_session_result_snapshot(session: Path, text: str) -> None:
    result_path = session / "result.md"
    existing = result_path.read_text(encoding="utf-8") if result_path.exists() else ""
    if text_is_pending(existing):
        result_path.write_text("# Result\n\n" + text.strip() + "\n", encoding="utf-8")
        return
    if "## Custom Workflow Result Snapshot" not in existing:
        result_path.write_text(
            existing.rstrip() + "\n\n## Custom Workflow Result Snapshot\n\n" + text.strip() + "\n",
            encoding="utf-8",
        )


def snapshot_runner_artifacts(root: Path, phase: Phase, recommended_status: str) -> None:
    session = wily.current_session_path(root, phase)
    if not session:
        return
    paths = workflow_paths(root, phase, session)
    text = material_workflow_result([paths["external_result"], paths["session_result"]])
    if text is None:
        return
    paths["external_result"].parent.mkdir(parents=True, exist_ok=True)
    paths["external_result"].write_text(text, encoding="utf-8")
    paths["session_result"].write_text(text, encoding="utf-8")
    write_session_result_snapshot(session, text)


def command_run(root: Path, args: list[str]) -> int:
    phase_id, workflow, autonomy_mode, dry_run, error = parse_args(args)
    if error:
        print(error, file=sys.stderr)
        return 2
    if not phase_id:
        print(
            "Usage: wily.py run <stage-id>/<phase-id> [--runner <external-workflow-id>] "
            "[--autonomy conservative|goal_scoped|yolo]",
            file=sys.stderr,
        )
        return 2

    autonomy_error = validate_autonomy(autonomy_mode)
    if autonomy_error:
        print(autonomy_error, file=sys.stderr)
        return 2

    roadmap = wily.load_roadmap(root)
    phases = roadmap.get("phases") or []
    phase = wily.find_phase(roadmap, phase_id)
    stage: dict[str, Any] | None = None
    stage_state: dict[str, Any] | None = None
    display_id = phase_id
    if phase is None:
        found = wily.find_stage_phase(root, roadmap, phase_id)
        if found:
            stage, phase, stage_state = found
            display_id = wily.stage_phase_display_id(roadmap, phase_id, stage, phase)
        else:
            stage_candidate = wily.find_stage(roadmap, phase_id)
            if stage_candidate and wily.is_v2_roadmap(roadmap):
                return wily.reject_v2_stage_execution(root, roadmap, stage_candidate)
            print(f"Phase not found: {phase_id}", file=sys.stderr)
            return 1
    if stage is not None:
        if not stage_phase_executable(root, roadmap, stage, phase):
            print(f"Phase is not executable: {display_id}", file=sys.stderr)
            return 1
        phase_for_workflow = {**phase, "id": display_id, "stage_id": stage.get("id", "")}
    else:
        if not phase_executable(phase, phases):
            print(f"Phase is not executable: {phase_id}", file=sys.stderr)
            return 1
        phase_for_workflow = phase

    engine = workflow_engine(workflow)
    if dry_run:
        request_path = root / "agent-handoffs" / f"{slugify_phase(phase_for_workflow)}-custom-workflow-request.md"
        result_path = root / "agent-handoffs" / f"{slugify_phase(phase_for_workflow)}-custom-workflow-result.md"
        print(f"Dry run: phase {display_id} is executable")
        print(f"Workflow engine: {engine}")
        print(f"Runner alias: {workflow}")
        print(f"Autonomy: {autonomy_mode}")
        print("Required Codex routing:")
        print(f"- {PRIMARY_SKILL}")
        print(f"- {PARALLEL_SKILL} when the execution package allows parallel lanes")
        print("Native goal command:")
        print(native_goal_command(phase_for_workflow, engine, autonomy_mode, request_path, result_path, root))
        return 0

    if stage is not None and stage_state is not None:
        session = ensure_stage_phase_session(root, roadmap, stage, phase, stage_state, display_id)
        phase_for_workflow = {**phase, "id": display_id, "stage_id": stage.get("id", "")}
    else:
        session = ensure_session(root, phase, roadmap)
        phase_for_workflow = phase
    artifacts = write_custom_workflow_request(root, phase_for_workflow, workflow, engine, autonomy_mode, session)
    goal_command = native_goal_command(
        phase_for_workflow,
        engine,
        autonomy_mode,
        artifacts["external_request"],
        artifacts["external_result"],
        root,
    )

    print(f"Prepared phase {display_id} for Custom Workflow Skillset")
    print(f"Workflow engine: {engine}")
    print(f"Runner alias: {workflow}")
    print(f"Autonomy: {autonomy_mode}")
    print(f"Session: {session}")
    print(f"Custom Workflow request: {artifacts['external_request']}")
    print(f"Result target: {artifacts['external_result']}")
    print("Required Codex routing:")
    print(f"- {PRIMARY_SKILL}")
    print(f"- {PARALLEL_SKILL} when the execution package allows parallel lanes")
    print("Native goal command:")
    print(goal_command)
    return 0


def main(argv: list[str] | None = None) -> int:
    return command_run(Path.cwd(), list(sys.argv[1:] if argv is None else argv))


if __name__ == "__main__":
    raise SystemExit(main())
