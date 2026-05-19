# wily-agent

Use `wily agent` to install and manage the bundled `wily-agent` heartbeat daemon.

Common commands:

```bash
wily agent check
wily agent configure --url https://board.example --repo OWNER/REPO --actor wily --secret "$WILY_BOARD_SECRET"
wily agent register --repo OWNER/REPO
wily agent install
wily agent start
wily agent status
wily agent stop
wily agent dev --once --offline-ok
```

The daemon is local-first and best-effort. Missing config, Board downtime, or
signature errors must not fail normal Wily task commands.
