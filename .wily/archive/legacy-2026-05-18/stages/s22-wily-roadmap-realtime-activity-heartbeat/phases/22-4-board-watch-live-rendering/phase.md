# Phase 22-4: Board and Wily Watch live rendering

## Purpose

Render realtime activity clearly in both Wily Board and `wily-watch`.

## Acceptance

- Board shows local-only activity awaiting push.
- Board renders one chip per `(actor, agent)` session.
- Board and Watch distinguish `working`, `active`, `idle`, and `stale`.
- `wily-watch` reads `.wily/local/live/active/*.json` without emitting network events.
- Durable roadmap progress stays visually separate from live session state.
