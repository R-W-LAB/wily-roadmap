# Wily Phase Context

Phase: 05-1 - wily-status에서 Roadmap 출력 예시 보여주기

## Phase

# Phase 05-1: wily-status에서 Roadmap 출력 예시 보여주기

## Purpose

`$wily-status`가 현재 로드맵의 흐름을 한 번에 이해할 수 있게 Roadmap 출력 예시를 직접 보여주는 방식으로 개선한다.

## Expected Starting Conditions

- Phases 04-1 and 04-2 are done.
- `scripts/wily.py status` and `scripts/wily_state_summary.py` are stable enough to revise output shape.

## Likely Files

- `scripts/wily.py`
- `scripts/wily_state_summary.py`
- `tests/test_wily_cli.py`
- `tests/test_wily_state_summary.py`
- `skills/wily-status/SKILL.md`

## Completion Criteria

- `$wily-status` output includes a clear Roadmap example or Roadmap-shaped summary once, without noisy duplication.
- The behavior is covered by focused tests.
- Output remains useful in Korean and still keeps helper details deterministic.
- Existing lifecycle and init behavior is preserved.

## Known Risks

- Status output can become too verbose if the Roadmap example duplicates the normal summary.
- Keep the command useful for repeated use, not only as a tutorial.

## Planner Adapter

# Planner Adapter

Recommended planner: superpowers:writing-plans

Use the planner before changing status output because the output contract is user-facing.

## Prompt

# Execution Prompt

Improve `$wily-status` so it shows Roadmap output once in a way that makes the current roadmap structure immediately visible.

Scope:
- Decide whether the Roadmap output belongs in `scripts/wily.py status`, `scripts/wily_state_summary.py`, or the status skill guidance.
- Add focused tests before implementation.
- Avoid duplicating the same roadmap content in multiple sections.
- Keep output readable in Korean.

## Verification

# Verification

Run:

```bash
python3 -m unittest tests.test_wily_cli tests.test_wily_state_summary
python3 -m unittest discover
python3 -m py_compile scripts/wily.py scripts/wily_state_summary.py
```

Also run `python3 scripts/wily.py status` in this repository and inspect the Roadmap output manually.

## Handoff

# Handoff

Start by capturing the current `$wily-status` output and identifying exactly what should be shown once as the Roadmap view.

This phase can run in parallel with phase 05-2.

## Existing Implementation Plan

# Implementation Plan

No detailed implementation plan exists yet.

Generate one before editing status output behavior.
