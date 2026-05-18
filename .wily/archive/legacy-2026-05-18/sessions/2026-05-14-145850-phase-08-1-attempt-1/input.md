# Wily Phase Context

Phase: 08-1 - Watch pane Stage별 접기 펼치기 인터랙션

## Phase

# Phase 08-1: Watch pane Stage별 접기 펼치기 인터랙션

## Purpose

`$wily-watch` pane에서 완료된 stage summary나 stage header를 마우스 클릭 또는 키보드로 접었다 펼칠 수 있게 한다.

## Dependencies

- 06-5 긴 로드맵 Pane에서 완료 Stage 접기 전략

## Parallel Group

08

## Expected Starting Conditions

- Watch pane already collapses leading completed stages when height is constrained.
- `$wily-watch` opens a tmux pane by default and supports `--here`, `--once`, `--ui`, and `--interval`.
- Current renderer is deterministic for non-interactive tests.

## Expected Output

- Interactive watch mode supports stage expand/collapse.
- Mouse click on a folded done summary or stage row toggles that stage group when terminal/tmux mouse events are available.
- Keyboard fallback exists, at minimum `d` for done-stage expand/collapse and `q` to quit.
- Footer tells the user the available interaction: click or key toggle, refresh, quit.
- `--once` remains deterministic and non-interactive.
- Tests cover input parsing/state transitions without requiring real mouse hardware.

## Likely Files

- `scripts/wily.py`
- `scripts/wily_watch_ui.py`
- `tests/test_wily_cli.py`
- `tests/test_wily_watch_ui.py`
- `skills/wily-watch/SKILL.md`

## Known Risks

- Terminal mouse reporting differs by terminal/tmux settings.
- Raw terminal mode must be restored on exit.
- Mouse support should not make `$wily-watch --once` flaky.
- If click support is unavailable, keyboard fallback must still work.

## Planner Adapter

# Planner Adapter

Recommended planner: superpowers:writing-plans

Use the planner because terminal mouse interaction needs a precise input/rendering contract before implementation.

## Prompt

# Execution Prompt

Add interactive stage expand/collapse to `$wily-watch`.

Scope:
- Preserve deterministic `--once` output.
- Add interactive state for stage/done-summary expansion in continuous watch mode.
- Support mouse click toggles where terminal/tmux mouse events are available.
- Add keyboard fallback for the same behavior.
- Restore terminal modes and mouse reporting on exit.
- Update `$wily-watch` guidance and focused tests.

## Verification

# Verification

Run:

```bash
python3 -m unittest tests.test_wily_watch_ui tests.test_wily_cli
python3 -m unittest discover
python3 -m py_compile scripts/wily.py scripts/wily_watch_ui.py
```

Manually inspect:

```bash
./wily watch --once --ui ascii
```

If interactive mode is implemented, manually run `$wily-watch` or `./wily watch --here` in a tmux pane and verify:

- click toggles folded completed stage details,
- keyboard fallback toggles the same state,
- `q` or `Ctrl-C` exits and restores terminal behavior.

## Handoff

# Handoff

Start by designing the interaction contract.

Recommended direction:

- Keep `--once` non-interactive.
- Add an internal watch state object that tracks expanded/collapsed stage IDs or the leading done summary.
- Parse terminal mouse escape events in a small pure helper so tests can feed fixture strings.
- Add keyboard fallback before relying on mouse-only behavior.
- Make footer text reflect current state, for example `click/d expand done · r refresh · q quit`.

## Existing Implementation Plan

# Implementation Plan

No detailed implementation plan exists yet.

Generate one before changing watch interactivity.
