# Wily Phase Context

Phase: 09-6 - Optional runner hooks와 watch progress 후속 통합

## Phase

# Phase 09-6: Optional runner hooks와 watch progress 후속 통합

## Purpose

Bundled runner v1 이후, opt-in hooks와 `wily-watch` runner progress 표시를 검토하고 구현한다.

## Source Spec

- `docs/superpowers/specs/2026-05-14-wily-bundled-runner-architecture.md`

## Dependencies

- 09-5 Runner artifact archive와 review handoff 연결

## Expected Output

- Hooks remain opt-in and respect Wily autonomy mode.
- PostToolUse evidence capture can update runner verification artifacts when enabled.
- Stop continuation guard can understand Wily phase status and autonomy mode when enabled.
- `wily-watch` can show runner progress from status artifacts if this remains useful.

## Known Risks

- Hooks, MCP servers, and app integrations must not become required for core Wily behavior.
- This is explicitly not part of first bundled runner implementation.

## Planner Adapter

# Planner Adapter

Recommended planner: superpowers:writing-plans

Use the planner because this phase is intentionally later and should reassess actual runner usage first.

## Prompt

# Execution Prompt

Evaluate and implement optional runner hooks and watch progress integration after bundled runner v1 is stable.

Scope:
- Keep hooks opt-in.
- Respect Wily autonomy mode.
- Do not require hooks for core Wily commands.
- Add `wily-watch` runner progress only if the session runner artifacts are stable enough.

## Verification

# Verification

Run the focused tests for any hook or watch changes introduced in this phase.

At minimum:

```bash
python3 -m unittest discover
```

## Handoff

# Handoff

Do not start this phase until 09-5 is complete and runner artifact formats have been exercised.

## Existing Implementation Plan

# Implementation Plan

No detailed implementation plan exists yet.
