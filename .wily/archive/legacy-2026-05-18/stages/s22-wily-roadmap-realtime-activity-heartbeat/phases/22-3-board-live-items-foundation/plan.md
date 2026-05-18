# Implementation Plan

1. Add failing Board tests for the new item-scoped live contract:
   - item payloads can target a Stage without `phase_id`
   - legacy phase payloads still store the existing `live_sessions` row
   - every accepted event also stores an item-scoped `live_items` row
   - duplicate events update the same `session_id` row
   - `worked` events update `last_worked_at`
   - server timestamps ignore `client_time`
2. Add the Board schema and repository helpers for `live_items`.
3. Update the live event API validation so either legacy `phase_id` or new `item_type`/`item_id` identity is accepted.
4. Dual-write legacy phase events into `live_sessions` and `live_items`; write Stage-only events only into `live_items`.
5. Add `LIVE_WORK_SECONDS` config with the default work window.
6. Run targeted red/green tests, expanded Board live/web tests, then the full Board test suite.
