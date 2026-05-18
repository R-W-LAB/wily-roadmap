# Wily Phase Context

Phase: 14-1 - Stage와 Phase 계층 분리 및 Stage 분해 skill 추가

## Phase

# Phase 14-1: Stage와 Phase 계층 분리 및 Stage 분해 skill 추가

## Purpose

Wily의 계획 단위를 두 계층으로 분리한다. `$wily-init`은 전체 목표를 큰 Stage들로 나누고, 각 Stage를 시작할 때 별도 문제 분해 skill이 Stage 내부를 실행 가능한 Phase DAG로 나누게 한다.

## Dependencies

- 13-1 roadmap YAML 블록 문법 데이터 손실 방지

## Expected Output

- `.wily/roadmap.yaml` 또는 보조 상태 파일에서 Stage와 Phase의 의미가 명확히 구분된다.
- `$wily-init`은 repo 전체 목표를 Stage 수준으로만 작성하고, Stage 내부 Phase를 과도하게 선작성하지 않는다.
- 새 skill은 Stage 시작 시 현재 Stage의 목적, 제약, 완료 조건을 읽고 내부 Phase 목록과 의존성을 생성한다.
- 기존 Phase 기반 명령은 하위 호환되며, 기존 `.wily` state를 깨지 않는다.
- `$wily-next`, `$wily-status`, `$wily-watch`는 Stage-only 상태와 Stage 내부 Phase 상태를 모두 읽을 수 있다.
- local-first 및 approval-first 원칙을 유지하고 remote 동작은 추가하지 않는다.

## Likely Files

- `plugins/wily-roadmap/skills/wily-init/SKILL.md`
- `plugins/wily-roadmap/skills/wily-workflow/SKILL.md`
- `plugins/wily-roadmap/skills/<new-stage-decomposition-skill>/SKILL.md`
- `plugins/wily-roadmap/scripts/wily.py`
- `plugins/wily-roadmap/scripts/wily_state_summary.py`
- `plugins/wily-roadmap/scripts/wily_watch_ui.py`
- `tests/`

## Known Risks

- Stage와 기존 `parallel_group` 기반 stage 표현이 혼동될 수 있다.
- 기존 roadmap serializer가 새 계층 필드를 손실하지 않도록 테스트가 필요하다.
- Stage 시작 시 Phase를 생성하는 명령이 기존 `$wily-start`와 역할 충돌을 일으킬 수 있다.

## Planner Adapter

# Planner

Recommended planner: superpowers:writing-plans

Use a short design pass before implementation:

- Define the state schema for Stage-only roadmap entries and Stage-internal Phase entries.
- Decide the user-facing skill name and command flow for Stage decomposition.
- Add focused tests for reading old roadmaps, writing new Stage fields, and selecting the next executable unit.
- Keep the implementation local-first and approval-first.

## Prompt

# Execution Prompt

Implement Stage/Phase separation for Wily roadmap planning.

Scope:

- Treat Stage as the top-level roadmap unit created by `$wily-init`.
- Add a new Stage decomposition skill that runs when starting a Stage and breaks that Stage into executable Phase work.
- Preserve compatibility with existing Phase-only roadmaps.
- Update status/watch/next behavior so Stage-only and Stage-with-Phases states remain understandable.
- Add tests for schema parsing, lifecycle transitions, and migration compatibility.
- Do not add hooks, MCP servers, app integrations, or remote actions.

Before editing, confirm the exact skill name and CLI entry point from local conventions, then implement the smallest coherent path.

## Verification

# Verification

Run focused tests for roadmap parsing and lifecycle behavior:

```bash
python3 -m unittest tests.test_wily_state_summary tests.test_wily_cli
python3 -m py_compile plugins/wily-roadmap/scripts/wily.py plugins/wily-roadmap/scripts/wily_state_summary.py plugins/wily-roadmap/scripts/wily_watch_ui.py
```

Then run the full suite:

```bash
python3 -m unittest discover
```

Expected:

- old Phase-only roadmaps still parse and render;
- new Stage-level roadmaps can be initialized without premature Phase expansion;
- Stage decomposition creates executable internal Phase work without losing Stage metadata;
- next/status/watch remain readable at both levels.

## Handoff

# Handoff

Start by reading the current `$wily-init`, `$wily-start`, `$wily-next`, `$wily-status`, and `$wily-watch` skill contracts. Identify where the existing code uses `stage_groups` from `parallel_group`, then introduce a distinct Stage concept without breaking that display grouping.

## Existing Implementation Plan

# Implementation Plan

No detailed implementation plan exists yet.
