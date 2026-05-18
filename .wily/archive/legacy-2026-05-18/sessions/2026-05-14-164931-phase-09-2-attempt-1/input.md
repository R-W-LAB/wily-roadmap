# Wily Phase Context

Phase: 09-2 - Custom Workflow bundled runner 파일 구성

## Phase

# Phase 09-2: Custom Workflow bundled runner 파일 구성

## Purpose

Custom Workflow runner assets를 `runners/custom-workflow/` 아래에 bundled runner로 배치한다.

## Source Spec

- `docs/superpowers/specs/2026-05-14-wily-bundled-runner-architecture.md`

## Dependencies

- 09-1 Runner adapter 계약과 Custom Workflow manifest 정의

## Parallel Group

09

## Expected Output

- `runners/custom-workflow/skills/*`
- `runners/custom-workflow/agents/*.toml`
- `runners/custom-workflow/scripts/status_board.py`
- `runners/custom-workflow/scripts/validate_execution_package.py`
- `runners/custom-workflow/scripts/watch_status.py`
- optional `runners/custom-workflow/hooks/hooks.json`
- Top-level skill wrappers only if Codex discovery requires them.

## Known Risks

- Do not auto-install hooks globally.
- Keep runner-local files canonical unless a later decision changes that.

## Planner Adapter

# Planner Adapter

Recommended planner: superpowers:writing-plans

Use the planner if the source Custom Workflow bundle needs inventory and file mapping.

## Prompt

# Execution Prompt

Bundle Custom Workflow runner files under `runners/custom-workflow/`.

Scope:
- Keep bundled runner files separate from Wily core.
- Preserve `.codex-plugin/plugin.json`, `skills/`, `.claude-plugin/plugin.json`, and `commands/` compatibility.
- Do not install or activate hooks automatically.

## Verification

# Verification

Run:

```bash
python3 -m compileall -q runners/custom-workflow
python3 runners/custom-workflow/scripts/validate_execution_package.py runners/custom-workflow/skills/plan-goal-runner/templates/execution-package.md
```

Adjust the second command if the template path differs after bundling.

## Handoff

# Handoff

Read the architecture spec and `runners/custom-workflow/runner.yaml` from 09-1 first.

This phase is file layout and bundle integrity only; command dispatch belongs to 09-4.

## Existing Implementation Plan

# Implementation Plan

No detailed implementation plan exists yet.
