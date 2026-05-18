# Phase 23-2: Board live draft storage and API

## Purpose

Teach Board to validate and persist stage decomposition draft events separately from presence events.

## Scope

- Add `live_drafts`.
- Validate `draft_kind=stage_decomposition`.
- Store accepted draft payloads.
- Reject malformed drafts.
