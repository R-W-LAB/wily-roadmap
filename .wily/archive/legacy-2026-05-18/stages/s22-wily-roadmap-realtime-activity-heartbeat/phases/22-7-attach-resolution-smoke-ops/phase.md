# Phase 22-7: Attach resolution, smoke, and operations docs

## Purpose

Connect provisional live activity to durable GitHub sync and document operations.

## Acceptance

- Board attaches local overlays after push using event-stream `current_item_id`.
- Replan rename does not break attach.
- Durable `.wily` YAML contains no live session fields.
- End-to-end smoke covers local-only work, Codex and Claude activity, stale transition, push attach, and secret rotation.
- Operations docs cover setup, troubleshooting, and HMAC rotation.
