# Phase 16-1: Board live session storage and signed event API

## Purpose

Add the Board-side storage and signed ingestion path for provisional live work events.

## Acceptance

- Board has a `live_sessions` table initialized with the app schema.
- `POST /api/live/events` accepts signed events and rejects invalid signatures.
- Accepted events upsert current live state without mutating durable `stages` or `phases`.
- GitHub sync clears matching `completed_local` or `blocked_local` overlays when durable state catches up.
