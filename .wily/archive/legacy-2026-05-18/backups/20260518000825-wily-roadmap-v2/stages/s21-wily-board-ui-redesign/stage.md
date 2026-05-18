# s21: Wily Board UI redesign

## Purpose

Redesign Wily Board so it works as a practical operating surface for daily roadmap coordination, not just a list of synced repositories.

Stage s22 has landed the realtime local activity foundation. The UI redesign should now render the final `live_items`, Wily Watch, heartbeat, and work-signal behavior produced by s22.

Revision 24 adds a required bridge between CustomWorkflow status boards and Wily Phase progress. CustomWorkflow may split a Wily Phase into checkpoint-sized execution steps, but those checkpoints currently live only in `agent-handoffs/*-status.md`. This Stage now makes that runner progress visible as a live Wily overlay in Roadmap, Watch, and Board while keeping durable Stage/Phase state authoritative.

The redesigned UI should make these questions easy to answer at a glance:

- What is active right now?
- What needs attention?
- Which repo or stage should be picked next?
- What is shared collaboration work versus personal work?
- Which status is durable Git state and which status is provisional live overlay?

## Scope

- Rework the Board dashboard information architecture around operational priority.
- Improve scanability for repo progress, active sessions, stale sessions, blockers, awaiting-push work, and unclaimed ready work.
- Render the Stage s22 live activity model cleanly: local-only entries, per-agent chips, `working` / `active` / `idle` / `stale` status, and durable sync attach state.
- Map CustomWorkflow checkpoint board rows to the selected Wily Stage/Phase/session as runner progress, not as permanent child Phases.
- Reflect current checkpoint, checkpoint progress, blocker, verification, and evidence links in Wily Roadmap/Watch and Board live surfaces.
- Clarify personal/shared filters and repo visibility without adding a workspace model.
- Keep durable `.wily` Git state visually distinct from live local overlay state.
- Preserve FastAPI, SQLite, GitHub App authentication for sync, and signed webhook/live-event architecture.
- Move the Board UI toward the read-only Next.js design in `docs/superpowers/specs/2026-05-16-wily-board-ui-redesign-design.md`.

## Non-Goals

- Do not replace `.wily` Git state as the source of truth.
- Do not add new MCP servers, hooks, app integrations, or workspace permissions.
- Do not redesign the Wily CLI watch pane in this stage.
- Do not bundle CustomWorkflow internals into Wily core; read runner artifacts through a small adapter contract.
- Do not auto-complete durable Wily Phases from checkpoint completion alone.
- Do not keep inline Board mutation controls in the redesigned UI. If GitHub App token code is still needed for sync, move it out of the PR-writing action boundary instead of deleting the shared auth path.
- Do not invent another live activity model; consume the model delivered by Stage s22.

## Source Spec

- `docs/superpowers/specs/2026-05-16-wily-board-ui-redesign-design.md`

That design supersedes the older calm-dashboard htmx spec for s21. The first phase must reconcile the spec with the current `R-W-LAB/wily-board` code before implementation.

## Child Phases

- 21-1 Contract reconciliation and implementation plan.
- 21-2 CustomWorkflow checkpoint-to-Phase contract.
- 21-3 Wily live checkpoint adapter.
- 21-4 Board checkpoint storage and SSE API.
- 21-5 Next.js scaffold and auth bridge.
- 21-6 Hub and Global MY DESK checkpoint surface.
- 21-7 Repo workspace Phase and checkpoint view.
- 21-8 Preferences, checkpoint polish, and responsive QA.
- 21-9 Read-only cutover, operations, and visual QA.
