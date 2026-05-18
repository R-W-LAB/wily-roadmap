# Wily Phase Context

Phase: 05-2 - 긴 Phase 제목 표시 방식 개선 검토

## Phase

# Phase 05-2: 긴 Phase 제목 표시 방식 개선 검토

## Purpose

Phase 제목이 길 때 `...`로 잘리는 현재 표시 방식을 검토하고, 정보를 덜 잃는 표시 전략으로 개선한다.

## Expected Starting Conditions

- Phases 04-1 and 04-2 are done.
- Current status/watch output can already show stage-based roadmap flow.

## Likely Files

- `scripts/wily_state_summary.py`
- `scripts/wily_watch_ui.py`
- `tests/test_wily_state_summary.py`
- `tests/test_wily_watch_ui.py`
- `skills/wily-status/SKILL.md`
- `skills/wily-watch/SKILL.md`

## Completion Criteria

- Long Phase titles are handled with a deliberate strategy instead of losing key context through blunt `...` truncation.
- The selected approach works for terminal width constraints.
- Tests cover long Korean and English titles where practical.
- Status and watch output remain readable and stable.

## Known Risks

- Removing truncation entirely can break compact watch layouts.
- Wrapping, middle truncation, and detail lines each have different tradeoffs; choose based on the actual UI surface.

## Planner Adapter

# Planner Adapter

Recommended planner: superpowers:writing-plans

Use the planner because this phase needs a small design decision before implementation.

## Prompt

# Execution Prompt

Review and improve how long Phase titles are displayed when they currently become `...`.

Scope:
- Find where title truncation happens in status and watch output.
- Compare practical options: wrapping, middle truncation, preserving full title in a detail line, or width-aware fallback.
- Add focused tests before implementation.
- Keep terminal output stable and readable.

## Verification

# Verification

Run:

```bash
python3 -m unittest tests.test_wily_state_summary tests.test_wily_watch_ui
python3 -m unittest discover
python3 -m py_compile scripts/wily_state_summary.py scripts/wily_watch_ui.py
```

Also inspect representative status/watch output with a long Korean Phase title.

## Handoff

# Handoff

Start by locating the exact truncation logic and capturing one current example where a long Phase title becomes `...`.

This phase can run in parallel with phase 05-1.

## Existing Implementation Plan

# Implementation Plan

No detailed implementation plan exists yet.

Generate one before editing title display behavior.
