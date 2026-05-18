# Verification

Verify the redesigned Board UI with:

- FastAPI JSON API tests for visible repos, desk data, repo detail, phase detail, and SSE event framing.
- Wily adapter tests that parse a CustomWorkflow status board and attach checkpoint state to the active Wily Phase without marking the Phase done.
- Wily Watch/status output tests that render current checkpoint, next checkpoint, blocker, and evidence under the attached Phase.
- Board live event/API tests for checkpoint started/completed/blocked/verification updates and durable sync reconciliation.
- Frontend tests or component-level checks for shared repos, personal repos, active sessions, stale sessions, blockers, awaiting-push items, and unclaimed ready work.
- Frontend tests or browser checks showing nested checkpoint progress under active Phase rows in both hub and repo workspace views.
- Repo workspace rendering that keeps durable status distinct from live overlay status.
- Desktop and mobile browser screenshots for the main dashboard and at least one repo detail page.
- A smoke check that no data-mutating UI remains in the redesigned Board.
- A deployment smoke proving Caddy/proxy routing and SSE buffering behavior.
