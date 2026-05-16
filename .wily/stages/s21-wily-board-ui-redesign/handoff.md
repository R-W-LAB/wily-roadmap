# Handoff

Stage s21 is pending behind Stage s22.

Do not start the UI redesign until the realtime activity heartbeat work is implemented. The redesign depends on the live model from Stage s22:

- `live_items` with session-scoped attach behavior
- local-only Stage/Phase entries before push
- per-agent `working`, `active`, `idle`, and `stale` chips
- Wily Watch rendering of the same local session registry

Start by reviewing the current Wily Board UI and the Stage s16-s20 behavior already implemented:

- live local overlay
- heartbeat freshness and stale presence
- collaboration operating surface
- critical path and risk view
- simple personal/shared visibility

The first implementation tranche should improve Board scanability without changing the source-of-truth model or adding new integration layers.
