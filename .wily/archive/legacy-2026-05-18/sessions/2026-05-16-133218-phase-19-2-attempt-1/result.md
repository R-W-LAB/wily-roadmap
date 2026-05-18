# Result

Implemented risk item query composition.

- Added `list_risk_items` for blocked phases, dependency bottlenecks, stale live sessions, awaiting-push completions, and unclaimed ready work.
- Risk items are sorted by deterministic severity and stable repo/stage/phase keys.
- Query uses only local SQLite state and live session timestamps.
