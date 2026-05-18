# Wily Phase Context

Phase: 09-5 - Runner artifact archive와 review handoff 연결

## Phase

# Phase 09-5: Runner artifact archive와 review handoff 연결

## Purpose

Runner output을 Wily session history 안에 durable archive로 남기고 review handoff 흐름을 연결한다.

## Source Spec

- `docs/superpowers/specs/2026-05-14-wily-bundled-runner-architecture.md`

## Dependencies

- 09-4 Runner dispatch helper 구현

## Expected Output

- `.wily/sessions/<session>/runner/` archive layout support
- `status.yaml` runner metadata recording
- Copy or snapshot runner artifacts at dispatch and finalization
- Completion/review handoff guidance for `needs_review`, `blocked`, and verified completion
- Tests proving `wily-run` does not mark phases done

## Known Risks

- Active runner-native files and durable Wily history must not diverge silently.
- Existing session history must remain readable.

## Planner Adapter

# Planner Adapter

Recommended planner: superpowers:writing-plans

Use the planner for archive timing and review-state decisions.

## Prompt

# Execution Prompt

Archive runner artifacts into Wily sessions and connect review handoff.

Scope:
- Add `.wily/sessions/<session>/runner/` artifact snapshot behavior.
- Record actual runner metadata in session status.
- Preserve completed phase/session history.
- Keep final `done` gated by verification evidence and Wily completion.

## Verification

# Verification

Run:

```bash
python3 -m unittest discover
python3 -m py_compile scripts/wily.py scripts/wily_runner.py
```

Skip `scripts/wily_runner.py` in the compile command if no dedicated helper exists.

## Handoff

# Handoff

Start from a working `wily-run` dispatch. Verify session metadata and runner archive paths before adding review states.

## Existing Implementation Plan

# Implementation Plan

No detailed implementation plan exists yet.
