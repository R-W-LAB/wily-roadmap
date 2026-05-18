# Result

Implemented Phase 16-3: Wily CLI best-effort live event emission.

- Added opt-in Board live config via `WILY_BOARD_URL`, `WILY_BOARD_SECRET`, `WILY_BOARD_REPO`, and `WILY_BOARD_ACTOR`.
- Added signed `emit_board_live_event` helper using `POST /api/live/events`.
- `$wily-start` emits `claimed` after successful local state writes.
- `$wily-complete` emits `completed_local` after successful local state writes.
- `$wily-block` emits `blocked_local` with the blocker reason after successful local state writes.
- Board network failures are best-effort and do not fail Wily lifecycle commands.
