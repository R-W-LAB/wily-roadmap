# Handoff

Stage s21 is now ready and decomposed. Stage s22 is complete, so the redesign can consume the final live activity model rather than guessing around it.

The redesign depends on the live model from Stage s22:

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

The first implementation tranche is 21-1. It should reconcile the design spec with the current `wily-board` codebase before any broad implementation:

- The design moves from htmx/Jinja to Next.js. Treat this as the new s21 direction.
- The design removes Board mutation controls. Remove routes/forms only at cutover, and preserve any GitHub App token code still needed for GitHub sync.
- Lock the SSE path and deployment/proxy shape before downstream frontend work.
- Keep durable `.wily` Git state visually distinct from provisional local live overlays.
