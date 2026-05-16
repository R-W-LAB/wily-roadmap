# Phase 21-7: Read-only cutover, operations, and visual QA

## Purpose

Cut over production routing to the redesigned read-only Board and remove old mutation UI safely.

## Acceptance

- Next.js serves the production Board entrypoint behind the existing host/proxy plan.
- Jinja template routes and static CSS are removed only after the Next.js pages cover the accepted surfaces.
- `/actions/phase/status` and status-change forms are removed from the Board UI.
- Shared GitHub App token/auth code needed for sync remains available outside the deleted action-route boundary.
- Operations docs cover frontend build, service startup, Caddy routing, SSE buffering, and rollback.
- Browser QA captures desktop and mobile screenshots for the hub and at least one repo workspace.
- A smoke check confirms the redesigned Board exposes no data-mutating controls.
