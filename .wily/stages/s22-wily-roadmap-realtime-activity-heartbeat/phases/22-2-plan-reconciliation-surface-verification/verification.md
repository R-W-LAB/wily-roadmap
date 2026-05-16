# Verification

Verified:

- Board current live state is `live_sessions`, not `live_items`.
- Board current live payloads are phase-scoped and require `repo`, `phase_id`, `actor`, `event`, and `live_status`.
- Board focused live overlay tests pass: `8 passed, 2 warnings`.
- Codex CLI is `codex-cli 0.130.0`.
- Claude Code is `2.1.143`.
- `codex app-server` exists, but there is no `codex app-server run` subcommand.
- Codex App Server generated schema/types include `turn/started`, `hook/started`, `turn/completed`, `hook/completed`, `item/started`, `item/completed`, and `rawResponseItem/completed`.
- Codex hooks are enabled in local config, but no installed Wily hook file was found.
- Claude Code hook surfaces are available through settings/plugin examples, but no Wily-specific Claude hook is installed yet.
- Board defaults are currently `LIVE_FRESH_SECONDS=120` and `LIVE_STALE_SECONDS=300`.

Implementation constraints carried forward:

- Preserve existing Board live event compatibility.
- Add item-scoped live state for Stage and Phase rows.
- Use heartbeat-only mode as the baseline.
- Treat Codex/Claude hooks and Codex App Server as richer optional work-signal sources.
- Document HMAC setup and rotation after the final event contract is implemented.
