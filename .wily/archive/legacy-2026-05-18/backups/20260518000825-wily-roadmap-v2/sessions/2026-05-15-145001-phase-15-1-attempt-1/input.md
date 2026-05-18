# Wily Phase Context

Phase: 15-1 - Wily Board repository and contract baseline

## Phase

# Phase 15-1: Wily Board repository and contract baseline

## Purpose

Establish `wily-board` as a separate web application with explicit boundaries, project structure, and implementation assumptions derived from `docs/wily-board-plan.md`.

## Dependencies

- Stage s14 complete, because Wily Board depends on the Stage/Phase state model being stable enough to consume.

## Expected Output

- A separate `wily-board` repository or local implementation workspace is created or prepared.
- README and project metadata state that Wily Board is a cache and PR-writing dashboard, while `.wily/` files remain the source of truth.
- The chosen Python/FastAPI/SQLite/htmx stack is captured in project scaffolding.
- The unresolved operator decisions are listed before deployment work begins.

## Likely Files

- `wily-board/README.md`
- `wily-board/pyproject.toml`
- `wily-board/app/`
- `wily-board/tests/`

## Known Risks

- Implementing inside `wily-roadmap` would blur plugin and dashboard lifecycles.
- Creating a remote repository requires explicit user approval.
- GitHub org, visibility, and credential choices may block later phases.

## Planner Adapter

# Planner

Recommended planner: manual Codex implementation.

Keep this phase focused on repository boundaries and skeleton only. Do not build sync, auth, UI, or deployment logic here.

## Prompt

# Execution Prompt

Prepare the `wily-board` project baseline from `docs/wily-board-plan.md`.

Scope:

- Keep Wily Board separate from the `wily-roadmap` plugin.
- Add minimal FastAPI project structure, README, pyproject, and test layout.
- Document the source-of-truth and PR-writing constraints.
- List deployment blockers that need user-provided credentials or hostnames.

Do not create remote repositories, GitHub Apps, OAuth Apps, secrets, hooks, MCP servers, or direct pushes without explicit approval.

## Verification

# Verification

Expected checks:

```bash
python3 -m py_compile app/main.py
python3 -m pytest
```

Adjust commands to the final `wily-board` project tooling.

## Handoff

# Handoff

Start from `docs/wily-board-plan.md`, sections 1 through 5 and appendix C.

## Existing Implementation Plan

# Plan

No detailed implementation plan exists yet.
