# Stage 22 Surface Verification

Date: 2026-05-16

## Scope

This records the Phase 22-2 check before implementing realtime Wily Roadmap activity heartbeat across Wily Roadmap, Wily Watch, and Wily Board.

## Board State

Current Wily Board already has a live overlay, but it is phase-scoped:

- storage: `live_sessions`
- key: `(repo_id, phase_id, actor, session_path)`
- required event fields: `repo`, `phase_id`, `actor`, `event`, `live_status`
- supported claim/freshness flow: `POST /api/live/events` and `GET /api/live/claims`
- current defaults: `LIVE_FRESH_SECONDS=120`, `LIVE_STALE_SECONDS=300`

The Stage 22 target needs item-scoped live state:

- `item_type`: `stage` or `phase`
- `item_id`: Stage id or Phase id
- `session_id`: stable per active local work session
- `current_item_id`: current working item when an agent can identify it
- `worked`: token-zero signal that the agent actually started useful work
- server-clock `last_seen_at` and `last_worked_at`

Decision: Phase 22-3 should add a compatibility bridge instead of breaking existing live payloads. Existing phase-scoped events should still store/render correctly while new item-scoped payloads unlock Stage-level and Phase-level realtime activity.

## Codex Surface

Verified local tool state:

- `codex --version`: `codex-cli 0.130.0`
- `codex app-server --help`: app-server command is available and supports `--listen`.
- `codex app-server run --help`: no `run` subcommand exists.
- `codex app-server generate-json-schema --out <dir>` and `generate-ts --out <dir>` generated protocol files.

Verified notification methods include:

- `turn/started`
- `hook/started`
- `turn/completed`
- `hook/completed`
- `item/started`
- `item/completed`
- `rawResponseItem/completed`

Decision: Phase 22-6 must not depend on a nonexistent `codex app-server run` command. The bridge should connect to an already-running app-server endpoint, or to a Desktop-provided endpoint when available.

## Hook Surface

Local Codex config has `hooks = true`, but no installed Wily hook file was found.

Claude Code is available as `2.1.143`. Local plugin examples and settings files show hook support for command hooks including `PreToolUse`, `PostToolUse`, `Stop`, and `SessionStart`. No Wily-specific Claude hook is installed yet.

Decision: Phase 22-6 should install or document Wily hooks as opt-in agent work signal emitters, and the realtime feature must keep working in heartbeat-only mode when hooks are absent.

## Timing And Secrets

Current Board timing:

- fresh: 120 seconds
- stale: 300 seconds

Stage 22 target timing:

- active heartbeat period: short fixed interval
- work signal window: about 90 seconds
- stale expiration: about 300 seconds

Decision: Phase 22-3 should introduce explicit work-window handling instead of overloading existing freshness. Phase 22-7 should document the final env vars and HMAC secret rotation path.

## Verification Commands

Board focused tests:

```sh
uv run pytest tests/test_live_events.py tests/test_db.py::test_decorate_live_session_freshness_classifies_fresh_and_stale tests/test_db.py::test_list_live_claim_conflicts_ignores_self_and_stale_claims tests/test_web_routes.py::test_board_excludes_stale_live_session_from_active_and_allows_up_next tests/test_web_routes.py::test_repo_detail_renders_stale_live_session_with_last_seen_label
```

Result: `8 passed, 2 warnings`.

Wily smoke:

```sh
python3 plugins/wily-roadmap/scripts/wily.py status
python3 plugins/wily-roadmap/scripts/wily.py next
```

Result: Stage 22 renders as its own Stage section and 22-2 is the active phase.
