# Phase 21-2: FastAPI read-only JSON and SSE API

## Purpose

Add the read-only API contract that the Next.js Board can consume while existing template routes continue to work.

## Acceptance

- Authenticated JSON endpoints exist for `/api/me`, `/api/repos`, `/api/repos/{owner}/{name}`, `/api/repos/{owner}/{name}/phases/{phase_id}`, `/api/desk`, and `/api/repos/{owner}/{name}/desk`.
- The SSE endpoint uses one locked path and emits `live_item.updated`, `live_item.cleared`, `durable.synced`, and heartbeat events.
- Responses expose durable `.wily` state separately from live overlay state.
- FastAPI OpenAPI schema is generated cleanly for frontend type generation.
- CORS/cookie behavior works for the local Next.js origin.
- Existing Jinja routes and live event ingestion remain operational during this phase.
