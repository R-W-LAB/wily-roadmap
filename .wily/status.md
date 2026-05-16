# Wily Status

Roadmap version 24 is complete through Stage s20, Stage s22, and Stage s23. Stage s21 is now the next decomposed Stage.

Current baseline:
- Stage s15 is complete. `R-W-LAB/wily-board` exists as a separate FastAPI/SQLite/htmx dashboard and is deployed at `https://rnwlab.duckdns.org`.
- Existing Board sync reads committed `.wily/roadmap.yaml` and `.wily/**/stage.yaml` from GitHub after push-triggered signed webhooks.
- Stage s16 adds push-before-local work visibility as a provisional Board overlay while keeping committed `.wily` state authoritative.
- Phase 16-1 is implemented and verified: Board now has `live_sessions` storage, signed `POST /api/live/events`, live event audit logging, and durable-sync clearing for matching `completed_local` and `blocked_local` overlays.
- Phase 16-2 is implemented and verified: Board repo detail and Active right now views render provisional live chips without changing durable status/progress.
- Phase 16-3 is implemented and verified: Wily CLI emits best-effort signed live events from start, block, and complete when opt-in Board config is present.
- Phase 16-4 is implemented and verified: operations docs and a local HTTP smoke confirm CLI-to-Board live event delivery before push.
- Stage s17 is implemented and verified: Wily CLI now supports lightweight `live-heartbeat`; Board classifies live sessions as fresh, recent, or stale; stale sessions remain visible on repo detail but no longer occupy Active right now or block Up next.
- Stage s18 is implemented and verified: Board shows claim conflict warnings, a Needs follow-up queue, and repository sync health.
- Stage s19 is implemented and verified: Board shows deterministic Attention risk items for blockers, dependency bottlenecks, stale work, awaiting-push risk, and unclaimed ready work.
- Stage s20 is implemented and verified: shared repos are visible to `airmang` and `Julirsia`, while personal repos are visible only to `visible_to`; `All`, `Shared`, and `Mine` filters are available.
- Stage s22 is implemented and verified: local Stage/Phase work appears in `wily-watch` and Wily Board with session-scoped heartbeat, token-zero `worked` events, local-only overlays, and durable sync attach.
- Stage s23 is implemented and verified: local Stage decomposition now emits live draft topology, Wily Board stores it as provisional `live_drafts`, renders draft child phases before push, and clears drafts after durable GitHub sync.
- Stage s21 is ready and decomposed: redesign the Wily Board into a read-only multi-repo personal work dashboard using the Stage s22/s23 live activity model, FastAPI JSON/SSE APIs, and a Next.js frontend cutover.

Next action:
- Start Phase 21-1 to reconcile the redesign contract with the current `R-W-LAB/wily-board` codebase and write the implementation plan.
