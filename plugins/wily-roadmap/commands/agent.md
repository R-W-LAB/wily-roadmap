# wily-agent

Use `wily agent` to install and manage the bundled Wily Board v3 sync daemon.

In Codex, users can ask through the plugin command without knowing the plugin
filesystem path:

```text
$wily-agent status
$wily-agent install
$wily-agent start
```

Codex should resolve the plugin root and run the internal helper command.

Common commands:

```bash
wily agent check
wily agent login <one-time-code> --url https://board.example --actor wily
wily agent register --repo OWNER/REPO
wily agent install
wily agent start
wily agent status
wily agent stop
wily agent run --once --offline-ok
wily agent unregister
```

The daemon is local-first and best-effort. It publishes Board v3 snapshots and
heartbeats when logged in. Missing config, Board downtime, invalid tokens, or
legacy signature errors must not fail normal Wily task commands.
