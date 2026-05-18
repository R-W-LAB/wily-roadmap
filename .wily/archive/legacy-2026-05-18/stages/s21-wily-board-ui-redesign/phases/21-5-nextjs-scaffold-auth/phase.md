# Phase 21-5: Next.js scaffold and auth bridge

## Purpose

Create the Next.js frontend shell against the checkpoint-aware Board API.

## Scope

- Scaffold Next.js 15 with strict TypeScript and the selected styling system.
- Generate or define API types that include checkpoint overlay fields.
- Bridge authentication and cookie forwarding to the existing FastAPI backend.
- Keep existing Jinja routes available until cutover.
- Prepare hub and repo workspace routes for SSE-driven checkpoint updates.
