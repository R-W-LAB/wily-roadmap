# Result

Implemented Phase 17-1: Heartbeat event contract and Board freshness model.

- Added Board settings for `LIVE_FRESH_SECONDS` and `LIVE_STALE_SECONDS`.
- Confirmed signed heartbeat events update existing live sessions to `active`.
- Added deterministic freshness decoration from `last_seen_at`, including fresh/recent/stale classification and last-seen labels.
- Kept durable roadmap state separate from live heartbeat updates.
