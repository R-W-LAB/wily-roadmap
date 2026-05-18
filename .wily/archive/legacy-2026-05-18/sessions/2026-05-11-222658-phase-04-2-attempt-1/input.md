# Wily Phase Context

Phase: 04-2 - Harden lifecycle status CLI

## Phase

# Phase 04-2: Harden Lifecycle Status CLI

## Purpose

Improve confidence in Wily lifecycle commands and roadmap summaries.

## Expected Starting Conditions

- Phase 03 is done.
- Command skill contracts and tests are stable.

## Likely Files

- `scripts/wily.py`
- `scripts/wily_state_summary.py`
- `tests/test_wily_cli.py`
- `tests/test_wily_state_summary.py`
- `skills/wily-status/SKILL.md`
- `skills/wily-next/SKILL.md`
- `skills/wily-start/SKILL.md`
- `skills/wily-complete/SKILL.md`
- `skills/wily-block/SKILL.md`
- `skills/wily-retry/SKILL.md`
- `skills/wily-replan/SKILL.md`

## Completion Criteria

- Status output remains stable and useful for ready, blocked, superseded, and replacement phases.
- Lifecycle commands preserve session history and current phase state.
- Tests cover important parse, serialize, and session edge cases.
- Helper script output stays machine-facing and English.

## Known Risks

- The custom YAML-like parser is intentionally small; avoid expanding it into a fragile partial YAML implementation.
- Preserve compatibility with existing test fixtures and roadmap files.

## Planner Adapter

# Planner Adapter

Recommended planner: superpowers:writing-plans

Use the planner before changing lifecycle command behavior.

## Prompt

# Execution Prompt

Harden Wily lifecycle and status CLI behavior.

Scope:
- Add tests first for any lifecycle or summary edge case.
- Keep parsing and serialization simple.
- Preserve phase/session separation.
- Do not change command names or plugin entrypoints without explicit approval.

## Verification

# Verification

Run:

```bash
python3 -m unittest tests.test_wily_cli tests.test_wily_state_summary
python3 -m unittest discover
python3 -m py_compile scripts/wily.py scripts/wily_state_summary.py
```

## Handoff

# Handoff

This phase can run in parallel with phase 04-1 after phase 03 is done.

Begin with `tests/test_wily_cli.py` and `tests/test_wily_state_summary.py`, then inspect the related functions in `scripts/wily.py` and `scripts/wily_state_summary.py`.

## Existing Implementation Plan

# Implementation Plan

No detailed implementation plan exists yet.

Generate one before editing lifecycle script behavior.
