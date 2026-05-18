# s24: S21 realtime Board bridge end-to-end hardening

## Purpose

Close the gap where S21 checkpoint/live code can pass unit tests while the real Board still does not show active Codex or CustomWorkflow work in realtime.

This Stage turns `agent-handoffs/s21-realtime-board-bridge-requirements.md` into the acceptance baseline. Success means the full route is proven locally before any production smoke is claimed:

- `wily start` owns the active Stage/Phase live session.
- CustomWorkflow status board progress attaches to that live session.
- Codex hook `live-worked` signals attach to the same live session.
- Wily emits signed live checkpoint/work events.
- Board stores, streams, and renders the overlay without mutating durable `.wily` state.
- Board Hub, repo detail, and `wily status/watch` show the same current checkpoint/live state.

## Scope

- Add or harden repo-local `.wily/board.json` live configuration and `wily board check` diagnostics.
- Install and verify Codex hook wiring for `live-worked`.
- Attach `agent-handoffs/*-status.md` checkpoint state to the active Wily session.
- Emit and accept signed checkpoint live events for started, updated, completed, blocked, and verification changes.
- Expose checkpoint overlay state through Board JSON and SSE APIs.
- Render matching checkpoint/live state in Board Hub, repo detail, and Wily status/watch.
- Add local end-to-end verification before any production claim.
- Add approval-gated production smoke steps for URL/secret/deploy/restart/push-sensitive work.

## Non-Goals

- Do not make Board the source of truth for roadmap progress.
- Do not auto-complete durable Wily Phases from checkpoint completion alone.
- Do not push, deploy, restart production services, or write production secrets without explicit user approval.
- Do not add MCP servers or app integrations.
- Do not treat unit tests alone as realtime success.

## Requirement Reference

- `agent-handoffs/s21-realtime-board-bridge-requirements.md`

## Child Phases

- 24-1 Board live config, diagnostics, and hook contract.
- 24-2 Wily checkpoint session bridge.
- 24-3 Board checkpoint overlay API, SSE, and UI parity.
- 24-4 Local E2E proof and approval-gated production smoke.
