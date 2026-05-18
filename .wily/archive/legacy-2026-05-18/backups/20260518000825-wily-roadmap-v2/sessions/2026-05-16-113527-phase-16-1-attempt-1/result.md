# Result

Implemented Phase 16-1: Board live session storage and signed event API.

- Added `live_sessions` storage to Wily Board.
- Added DB helpers for live session upsert/list behavior.
- Added signed `POST /api/live/events` ingestion.
- Live events reject invalid signatures and store provisional sessions without mutating durable stage or phase state.
- Durable GitHub sync now clears matching `completed_local` overlays when a phase reaches `done`, and matching `blocked_local` overlays when a phase reaches `blocked`.
