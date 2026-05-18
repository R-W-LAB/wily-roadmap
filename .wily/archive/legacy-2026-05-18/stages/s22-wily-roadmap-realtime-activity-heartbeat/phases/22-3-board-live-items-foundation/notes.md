# Notes

Implemented the Board `live_items` foundation in `/Users/wilycastle/Code/projects/wily-board`.

Changes:

- Added `live_items` storage keyed by `(repo_id, session_id)`.
- Added item identity fields: `item_type`, `item_id`, `stage_id`, and `phase_id`.
- Added `last_seen_at` and `last_worked_at` server-clock timestamps.
- Added `upsert_live_item`, `list_live_items`, and `decorate_live_item_freshness`.
- Added work-window decoration through `is_working`, `work_age_seconds`, and `work_label`.
- Updated `/api/live/events` to accept either legacy `phase_id` payloads or item-scoped `item_type`/`item_id` payloads.
- Kept legacy `live_sessions` compatibility by dual-writing phase payloads.
- Stage-only item payloads do not create synthetic `live_sessions` rows.
- Added `LIVE_WORK_SECONDS`, defaulting to `90`.

Important carry-forward:

- Board rendering still reads the legacy `live_sessions` overlay. Phase 22-4 should switch/extend render queries to use `live_items`.
- Durable attach/clear behavior for `live_items` is intentionally deferred to Phase 22-7.
