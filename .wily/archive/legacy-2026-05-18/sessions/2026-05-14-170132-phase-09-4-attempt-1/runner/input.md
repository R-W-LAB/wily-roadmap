# Wily Runner Input

- Phase ID: `09-4`
- Phase title: `Runner dispatch helper 구현`
- Runner: `custom-workflow`
- Autonomy mode: `goal_scoped`
- Wily session: `.wily/sessions/2026-05-14-170132-phase-09-4-attempt-1`
- Git status: `23 changed file(s)`

## Native Goal Command

`/goal Execute Wily phase 09-4: Runner dispatch helper 구현. Use runner custom-workflow with goal_scoped autonomy. Read agent-handoffs/09-4-runner-dispatch-helper-execution-package.md. Do not mark the Wily phase done; record verification evidence and finish with a recommended Wily status.`

## Phase Context

# Wily Phase Context

Phase: 09-4 - Runner dispatch helper 구현

## Phase

# Phase 09-4: Runner dispatch helper 구현

## Purpose

`wily-run`이 phase, runner, autonomy mode를 해석하고 Custom Workflow 실행 패키지를 생성하도록 dispatch helper를 구현한다.

## Source Spec

- `docs/superpowers/specs/2026-05-14-wily-bundled-runner-architecture.md`

## Dependencies

- 09-2 Custom Workflow bundled runner 파일 구성
- 09-3 wily-run 명령과 skill 추가

## Expected Output

- `scripts/wily.py run` command or dedicated `scripts/wily_runner.py`
- Runner resolution order: CLI flag, phase metadata, project default, bundled default
- Autonomy resolution order: CLI flag, phase metadata, project default, runner default
- Start or attach a Wily session without marking the phase done
- Generate runner input and Custom Workflow execution package/status/progress/verification files
- Include exact `/goal` command when native goal invocation is unavailable

## Known Risks

- Keep `scripts/wily.py` focused on state transitions if dispatch logic grows.
- Dispatch should stop after preparing runner artifacts unless runtime continuation is explicitly safe.

## Planner Adapter

# Planner Adapter

Recommended planner: superpowers:writing-plans

Use the planner because this phase touches state transitions and artifact generation.

## Prompt

# Execution Prompt

Implement runner dispatch for `wily-run`.

Scope:
- Validate phase exists and is executable.
- Resolve runner and autonomy mode.
- Start or attach session using existing lifecycle behavior where possible.
- Build phase context bundle.
- Create runner-native handoff files and session runner input.
- Never mark a phase `done` directly from dispatch.

## Verification

# Verification

Run:

```bash
python3 -m unittest tests.test_wily_cli
python3 -m py_compile scripts/wily.py scripts/wily_runner.py
```

Skip `scripts/wily_runner.py` in the compile command if no dedicated helper is created.

## Handoff

# Handoff

Read the 09-1 contract, 09-2 runner manifest, and 09-3 command skill before editing dispatch code.

## Existing Implementation Plan

# Implementation Plan

Detailed plan:

- `docs/superpowers/plans/2026-05-14-wily-runner-dispatch-helper.md`
