# Result

Implemented claim conflict warnings for Stage 18.

- Board can query fresh live claims from other actors on the same phase.
- `GET /api/live/claims` returns signed, freshness-filtered claim data for Wily CLI.
- Repo detail rows render a `Claim conflict` chip when another fresh actor is active on the same phase.
- Wily CLI `start` performs a best-effort claim check and prints a non-fatal warning when Board reports another fresh actor.
- Stale claims are ignored by both Board conflict detection and the CLI warning path.
