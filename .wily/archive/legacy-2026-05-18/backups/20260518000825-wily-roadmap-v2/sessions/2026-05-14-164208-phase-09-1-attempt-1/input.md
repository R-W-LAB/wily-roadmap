# Wily Phase Context

Phase: 09-1 - Runner adapter 계약과 Custom Workflow manifest 정의

## Phase

# Phase 09-1: Runner adapter 계약과 Custom Workflow manifest 정의

## Purpose

Wily Roadmap을 roadmap/session protocol로 유지하면서, Custom Workflow를 bundled default runner로 연결하기 위한 최소 계약을 문서화한다.

## Source Spec

- `docs/superpowers/specs/2026-05-14-wily-bundled-runner-architecture.md`

## Dependencies

- 07-1 GitHub Issues 선택적 연동 계약 정의
- 08-1 Watch pane Stage별 접기 펼치기 인터랙션

## Parallel Group

09

## Expected Output

- `runners/custom-workflow/runner.yaml` 생성
- `skills/wily-workflow/references/runner-adapter-contract.md` 생성
- `skills/wily-workflow/SKILL.md`에서 runner contract reference 연결
- Wily core와 Custom Workflow runner의 책임 경계가 명확해야 한다.
- 기본 autonomy mode는 `goal_scoped`로 기록한다.

## Known Risks

- Custom Workflow 세부 구현을 Wily core에 섞으면 장기 runner 교체성이 깨진다.
- manifest가 구현 가이드로 비대해지면 adapter contract가 불안정해진다.

## Planner Adapter

# Planner Adapter

Recommended planner: superpowers:writing-plans

Use the planner to keep the contract and manifest small before implementation.

## Prompt

# Execution Prompt

Implement the document-and-contract phase for the bundled runner architecture.

Scope:
- Create `runners/custom-workflow/runner.yaml`.
- Create `skills/wily-workflow/references/runner-adapter-contract.md`.
- Update `skills/wily-workflow/SKILL.md` to reference the contract.
- Keep Custom Workflow as a bundled default runner, not Wily core logic.
- Preserve plugin discovery compatibility.

## Verification

# Verification

Run:

```bash
python3 -m unittest tests.test_wily_cli tests.test_wily_watch_ui
python3 -m py_compile scripts/wily.py
```

If a manifest parser or command skill parser is introduced, add and run focused tests for it.

## Handoff

# Handoff

Start by reading:

- `docs/superpowers/specs/2026-05-14-wily-bundled-runner-architecture.md`
- `skills/wily-workflow/SKILL.md`

Do not implement `wily-run` yet. This phase defines only the contract and manifest baseline.

## Existing Implementation Plan

# Implementation Plan

No detailed implementation plan exists yet.
