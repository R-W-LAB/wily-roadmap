# Phase 21-9: Read-only cutover, operations, and visual QA

## Purpose

Cut over the read-only checkpoint-aware Board and verify operations end to end.

## Scope

- Route production Board traffic to the Next.js frontend.
- Remove Jinja mutation UI and action routes only after read-only replacements are verified.
- Update deployment and operations docs for SSE, Caddy/proxy behavior, and checkpoint overlay troubleshooting.
- Capture desktop and mobile browser QA for hub and repo workspace views.
- Confirm durable Wily sync remains authoritative and checkpoint overlay reconciles correctly.
