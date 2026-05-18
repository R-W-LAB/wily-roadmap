# Wily Phase Context

Phase: 10-2 - Codex app 환경의 wily-watch 전략 확정

## Phase

# Phase 10-2: Codex app 환경의 wily-watch 전략 확정

## Purpose

Codex app 환경에서 `wily-watch`를 어떻게 보여주고 운영할지 결정하고, 필요한 최소 구현을 추가한다.

## Dependencies

- 10-1 Zip bootstrap에서 GitHub self-update 경로 제공

## Expected Output

- Codex app에서 tmux pane 기반 watch가 가능한지, 불편한지, 또는 별도 표시 전략이 필요한지 명확히 정리한다.
- `wily watch`의 app-friendly 모드를 설계한다.
- 필요하면 `--once`, `--here`, `--ui ascii|rich|auto`와 별도로 Codex app에 맞는 출력 옵션을 추가한다.
- README 또는 Wily skill guidance에 Codex app watch 사용 방식을 문서화한다.
- 기존 terminal/tmux watch UX를 깨지 않는다.

## Known Risks

- Codex app 환경은 터미널 pane, background process, browser/plugin UI의 제약이 일반 터미널과 다를 수 있다.
- Watch가 너무 많은 출력을 만들면 Codex 대화 흐름을 방해할 수 있다.
- app-specific behavior가 core Wily CLI를 복잡하게 만들 수 있다.

## Planner Adapter

# Planner

Start with a short investigation before implementation planning.

Questions to answer:

- Codex app에서 `tmux` pane을 기대해도 되는가?
- Codex in-app browser or app surface를 watch companion으로 쓸 수 있는가?
- Watch는 continuous UI가 필요한가, 아니면 app 환경에서는 periodic snapshot이 더 좋은가?
- Current `wily watch --once` output is good enough for app updates, or needs a compact mode?

After the investigation, use `superpowers:writing-plans` if code changes are needed.

## Prompt

# Execution Prompt

Decide and implement the Codex app strategy for `wily-watch`.

Scope:

- Inspect current watch behavior in `scripts/wily.py` and `scripts/wily_watch_ui.py`.
- Evaluate Codex app constraints for terminal panes and long-running watch output.
- Prefer a minimal app-friendly snapshot mode if continuous panes are brittle.
- Preserve existing tmux, `--here`, `--once`, and UI selection behavior.
- Document the recommended Codex app workflow.

Do not add MCP servers, app integrations, or browser UI unless the user explicitly asks for that layer.

## Verification

# Verification

Run watch-focused tests and the broader suite.

At minimum:

```bash
python3 -m unittest tests.test_wily_cli tests.test_wily_watch_ui
python3 -m unittest discover
```

Manual checks:

- Existing `./wily watch --once --ui ascii` output still works.
- Existing tmux pane behavior remains documented and unchanged unless intentionally revised.
- Any Codex app-friendly mode produces bounded output suitable for a conversation update.

## Handoff

# Handoff

Not started.

## Existing Implementation Plan

No implementation plan exists yet.
Use the recommended planner to create one if this phase needs a detailed plan.
