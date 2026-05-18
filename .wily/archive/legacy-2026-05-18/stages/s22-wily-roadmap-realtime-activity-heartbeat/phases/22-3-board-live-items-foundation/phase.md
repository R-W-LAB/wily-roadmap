# Phase 22-3: Board live_items foundation

## Purpose

Add the Board data model and event contract needed for local-only realtime activity.

## Acceptance

- `live_items` stores one row per live session using `session_id`.
- Freshness derives from server clock, not client clock.
- `worked` events update `last_worked_at`.
- Duplicate events are idempotent.
- Existing legacy live payloads remain accepted during migration.
