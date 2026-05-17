# Phase 24-2: Wily checkpoint session bridge

Attach runner progress and Codex activity to the active Wily live session.

Acceptance:

- `wily start` is the canonical session source for active Stage/Phase work.
- CustomWorkflow `agent-handoffs/*-status.md` checkpoint state attaches to that session.
- Codex `live-worked` hook activity attaches to that session.
- Signed checkpoint/work events are emitted for update, completion, blocker, and verification changes.
- Durable Wily Phase status is not changed by checkpoint progress alone.
- `wily status` and `wily watch` render the live checkpoint overlay.
