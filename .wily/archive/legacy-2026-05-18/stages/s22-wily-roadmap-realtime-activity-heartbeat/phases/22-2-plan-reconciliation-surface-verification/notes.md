# Notes

Completed the pre-implementation surface check.

Findings:

- Wily Board currently has a `live_sessions` overlay, not `live_items`.
- The current live event API requires `repo`, `phase_id`, `actor`, `event`, and `live_status`.
- Board currently deduplicates live rows by `(repo_id, phase_id, actor, session_path)`.
- Board freshness defaults are `LIVE_FRESH_SECONDS=120` and `LIVE_STALE_SECONDS=300`.
- Board focused live overlay tests pass on the current implementation.
- Codex CLI is `codex-cli 0.130.0`; Claude Code is `2.1.143`.
- `codex app-server` exists, but there is no `codex app-server run` subcommand.
- Codex App Server schema exposes `turn/started`, `hook/started`, `turn/completed`, `hook/completed`, `item/started`, `item/completed`, and `rawResponseItem/completed` notifications.
- Local Codex config has hooks enabled, but no installed Wily hook file was found.
- Claude Code exposes hook-related CLI behavior and local plugin examples show `PreToolUse`, `PostToolUse`, `Stop`, and `SessionStart` hook shapes, but Wily hooks are not installed yet.

Plan reconciliation:

- Phase 22-3 must migrate or bridge Board state from phase-scoped `live_sessions` to item-scoped live state that can represent both Stages and Phases.
- Phase 22-3 should keep backward compatibility for the current `phase_id`-based payloads while adding `item_type`, `item_id`, `session_id`, and `worked` support.
- Phase 22-4 must render local-only Stage/Phase activity without mutating durable roadmap progress.
- Phase 22-5 must emit sidecar heartbeats and active session registry files using server-clock timestamps.
- Phase 22-6 must treat hooks and App Server bridge as progressive signal sources over a heartbeat fallback.
- Phase 22-7 must verify attach-after-sync behavior and document HMAC setup plus rotation.
