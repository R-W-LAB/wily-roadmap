# Phase 16-2: Board live overlay query and UI chips

## Purpose

Render provisional live work overlays in Wily Board without changing durable status dots or progress counts.

## Acceptance

- Repo detail phase rows show live chips for uncleared live sessions.
- `Active right now` includes phases with live local work even when durable status is still pending.
- `Up next` does not present phases with active uncleared live work as immediately available.
