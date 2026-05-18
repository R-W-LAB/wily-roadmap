# Verification

Run focused verification for both Board and Wily Roadmap:

- Board DB tests for `live_items`, `session_id` uniqueness, `current_item_id`, dedup, server-clock freshness, and terminal-event stickiness.
- Board route/render tests for local-only Stage/Phase entries, multi-agent chips on one item, `working` vs `active` vs `idle` vs `stale`, stale demotion, and durable attach after sync.
- Wily CLI tests for board config loading, signed event emission, `created_local`, `claimed`, `renamed`, `completed_local`, `blocked_local`, `released`, and best-effort network failure behavior.
- `wily-watch` tests showing `.wily/local/live/active/*.json` sessions without mutating durable progress.
- Heartbeat sidecar tests for detached return, parent-shell PID exit, `.alive` cleanup, TTL expiry, `--foreground` SIGINT release, and orphan recovery.
- Hook and bridge tests proving `worked` events are emitted outside the model context.
- End-to-end smoke from local-only Stage before push through GitHub webhook attach, including a replan rename and a clean durable `.wily` diff with no live fields.
