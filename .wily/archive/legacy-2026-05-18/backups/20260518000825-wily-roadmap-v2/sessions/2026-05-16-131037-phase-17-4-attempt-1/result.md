# Result

Documented and verified Stage 17 heartbeat operations.

- Added heartbeat runbook guidance to Board operations docs.
- Documented 15-30 second recommended interval, `Ctrl-C` stop behavior, finite `--count` smoke usage, and cost profile.
- Documented `LIVE_FRESH_SECONDS` and `LIVE_STALE_SECONDS` server settings.
- Verified a local Board server accepts two signed heartbeat events from Wily CLI and stores one active live session with two live event records.
