# Verification Plan

1. Inspect the current Wily Board live overlay implementation.
   - confirm storage table shape and event API fields
   - confirm freshness/staleness behavior and existing tests
   - identify the migration path from `live_sessions` to item-scoped live state
2. Verify local agent surfaces before implementation.
   - Codex CLI and app-server command availability
   - Codex App Server notification method names
   - local Codex hook feature state
   - Claude Code hook availability and installed hook state
3. Reconcile timing and secret assumptions.
   - current Board freshness defaults
   - planned work/active/idle/stale windows
   - HMAC provisioning and rotation gaps
4. Record implementation deltas for Phases 22-3 through 22-7.
5. Run current Board focused tests and Wily status/next smoke checks.
