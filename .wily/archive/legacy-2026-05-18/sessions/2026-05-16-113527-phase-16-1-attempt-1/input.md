# Wily Phase Context

Phase: 16-1 - Board live session storage and signed event API

## Phase

# Phase 16-1: Board live session storage and signed event API

## Purpose

Add the Board-side storage and signed ingestion path for provisional live work events.

## Acceptance

- Board has a `live_sessions` table initialized with the app schema.
- `POST /api/live/events` accepts signed events and rejects invalid signatures.
- Accepted events upsert current live state without mutating durable `stages` or `phases`.
- GitHub sync clears matching `completed_local` or `blocked_local` overlays when durable state catches up.

## Planner Adapter

# Planner

Recommended planner: manual

## Prompt

# Execution Prompt

Implement Board live session storage and signed event ingestion in `/Users/wilycastle/Code/projects/wily-board`.

Do not modify Wily CLI emission or UI chips in this phase.

## Verification

# Verification

Run:

```sh
uv run pytest tests/test_live_events.py tests/test_db.py tests/test_webhook.py
```

Also run:

```sh
uv run python -m py_compile app/db/repo.py app/sync/webhook.py app/live/events.py
```

## Handoff

# Handoff

Read the live overlay design spec first. Implement only Board storage/API and durable-sync clear behavior.

## Existing Implementation Plan

# Implementation Plan

Use `docs/superpowers/plans/2026-05-16-wily-board-live-overlay.md`, Task 1.
