# Verification

Verify the redesigned Board UI with:

- FastAPI JSON API tests for visible repos, desk data, repo detail, phase detail, and SSE event framing.
- Frontend tests or component-level checks for shared repos, personal repos, active sessions, stale sessions, blockers, awaiting-push items, and unclaimed ready work.
- Repo workspace rendering that keeps durable status distinct from live overlay status.
- Desktop and mobile browser screenshots for the main dashboard and at least one repo detail page.
- A smoke check that no data-mutating UI remains in the redesigned Board.
- A deployment smoke proving Caddy/proxy routing and SSE buffering behavior.
