# Handoff

Stage s21 is now ready and decomposed. Stage s22 is complete, so the redesign can consume the final live activity model rather than guessing around it.

The redesign depends on the live model from Stage s22:

- `live_items` with session-scoped attach behavior
- local-only Stage/Phase entries before push
- per-agent `working`, `active`, `idle`, and `stale` chips
- Wily Watch rendering of the same local session registry

Revision 24 adds a new prerequisite inside s21: CustomWorkflow checkpoint boards must become Phase-linked live progress. The current s21 run shows the drift this must fix: `agent-handoffs/s21-board-ui-redesign-status.md` has checkpoint progress through API implementation while `.wily/stages/s21-wily-board-ui-redesign/stage.yaml` only knows about Wily Phase `21-1`.

Use that drift as a fixture, not as a reason to manually flatten every checkpoint into a durable Phase. The intended model is:

- Wily Stage/Phase/session remains the durable roadmap unit.
- CustomWorkflow checkpoint rows become live runner overlay attached to the selected Phase.
- Board and Wily Watch show current checkpoint/action/evidence in realtime.
- Wily Phase completion still requires the normal verified Wily lifecycle.

Start by reviewing the current Wily Board UI and the Stage s16-s20 behavior already implemented:

- live local overlay
- heartbeat freshness and stale presence
- collaboration operating surface
- critical path and risk view
- simple personal/shared visibility

The first implementation tranche after 21-1 is now 21-2. It should reconcile CustomWorkflow checkpoint status boards with Wily Phase ownership before broad frontend work continues:

- The design moves from htmx/Jinja to Next.js. Treat this as the new s21 direction.
- The design removes Board mutation controls. Remove routes/forms only at cutover, and preserve any GitHub App token code still needed for GitHub sync.
- Lock the SSE path and deployment/proxy shape before downstream frontend work.
- Keep durable `.wily` Git state visually distinct from provisional local live overlays.
