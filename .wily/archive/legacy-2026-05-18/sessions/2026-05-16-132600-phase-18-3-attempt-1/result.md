# Result

Implemented the repository sync health panel.

- Added `list_repo_health` to classify registered repositories as `ok`, `stale`, or `not_initialized`.
- Health classification uses stage count, `last_synced_at`, and a 24-hour stale threshold.
- Dashboard now renders a read-only `Sync health` section with repo links, status chips, stage counts, and last sync timestamps.
