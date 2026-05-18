# Phase 16-3: Wily CLI best-effort live event emission

## Purpose

Send signed live work events from Wily lifecycle commands when Board live sync is explicitly configured.

## Acceptance

- No network call occurs when Board live config is absent.
- `$wily-start` emits `claimed`.
- `$wily-block` emits `blocked_local` with reason.
- `$wily-complete` emits `completed_local`.
- Board failures do not fail local lifecycle commands.
