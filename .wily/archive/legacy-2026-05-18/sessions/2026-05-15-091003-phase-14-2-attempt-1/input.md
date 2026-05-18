# Wily Phase Context

Phase: 14-2 - 스마트폰 Codex 앱용 하단 가로 watch pane 레이아웃

## Phase

# Phase 14-2: 스마트폰 Codex 앱용 하단 가로 watch pane 레이아웃

## Purpose

스마트폰의 Codex 앱에서 `$wily-watch`가 세로 side pane이 아니라 하단 horizontal pane으로 열리게 하고, 낮은 높이와 넓은 가로 흐름에 맞춘 전용 watch 레이아웃을 제공한다.

## Dependencies

- 13-1 roadmap YAML 블록 문법 데이터 손실 방지

## Expected Output

- Codex 앱 또는 좁은/mobile 환경을 감지하거나 명시 옵션으로 선택해 tmux split을 하단 horizontal pane으로 연다.
- 하단 pane에서는 기존 세로 pipeline 대신 현재 Stage, ready Phase, pending 요약을 가로 폭 중심으로 압축 표시한다.
- 낮은 높이에서도 header, progress, frontier, footer가 겹치거나 잘리지 않는다.
- 기존 데스크톱/tmux side pane watch 동작은 유지된다.
- `--dry-run-pane` 또는 렌더 함수 테스트로 horizontal split 명령과 layout 선택을 검증한다.

## Likely Files

- `plugins/wily-roadmap/skills/wily-watch/SKILL.md`
- `plugins/wily-roadmap/scripts/wily.py`
- `plugins/wily-roadmap/scripts/wily_watch_ui.py`
- `tests/test_wily_cli.py`
- `tests/test_wily_watch_ui.py`

## Known Risks

- Codex 앱의 실제 모바일 터미널 특성은 환경 변수만으로 안정적으로 구분하기 어려울 수 있다.
- tmux split 방향 변경은 기존 사용자 muscle memory와 충돌할 수 있으므로 명시 옵션 또는 신중한 자동 감지가 필요하다.
- 낮은 pane 높이에서 rich UI 스타일이 오히려 정보를 가릴 수 있다.

## Planner Adapter

# Planner

Recommended planner: superpowers:test-driven-development

Use TDD around command selection and render behavior:

- Add tests for tmux pane command direction selection.
- Add watch render snapshots for short horizontal pane sizes.
- Add regression coverage that desktop side pane behavior remains unchanged unless mobile/bottom mode is selected.

## Prompt

# Execution Prompt

Implement smartphone Codex app support for `$wily-watch`.

Scope:

- Make watch open as a bottom horizontal pane for smartphone/Codex app usage, either through reliable detection or an explicit option with safe defaults.
- Add a width-first compact layout for short horizontal panes.
- Preserve existing desktop side-pane behavior unless the new mode is selected or confidently detected.
- Add tests for dry-run pane commands and render output at mobile-like dimensions.
- Keep the change local-first and avoid hooks, MCP servers, or app integrations.

Pay special attention to text cropping and footer behavior in very short panes.

## Verification

# Verification

Run focused watch tests:

```bash
python3 -m unittest tests.test_wily_cli tests.test_wily_watch_ui
python3 -m py_compile plugins/wily-roadmap/scripts/wily.py plugins/wily-roadmap/scripts/wily_watch_ui.py
```

Then run the full suite:

```bash
python3 -m unittest discover
```

Expected:

- dry-run pane command uses the intended bottom horizontal split mode for smartphone/Codex app watch;
- compact horizontal layout fits short pane heights;
- existing side-pane watch behavior remains covered.

## Handoff

# Handoff

Start with `tmux_watch_command`, `command_watch_pane`, and `wily_watch_ui.render_watch`. Keep the default desktop behavior stable while adding a deliberate path for smartphone/Codex app bottom-pane rendering.

## Existing Implementation Plan

# Implementation Plan

No detailed implementation plan exists yet.
