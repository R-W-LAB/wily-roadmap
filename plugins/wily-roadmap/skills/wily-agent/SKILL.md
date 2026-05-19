---
name: wily-agent
description: Use when installing, configuring, checking, starting, stopping, or debugging the bundled Wily Roadmap heartbeat daemon.
---

# Wily Agent

Manage the local `wily-agent` daemon that watches registered `.wily` repositories
and sends best-effort signed heartbeat/live events to Wily Board.

## Internal Command

```bash
python3 <plugin-root>/scripts/wily.py agent <install|configure|register|start|stop|status|check|dev>
```

## Behavior

- `install` writes the macOS launchd plist.
- `configure` writes local Board URL, repo, actor, secret, and interval config.
- `register` adds the current `.wily` repo to the local registry.
- `start` and `stop` manage the launchd daemon.
- `status` prints install, config, registry, and daemon state.
- `check` runs a smoke check and stays best-effort when not configured.
- `dev` runs the foreground daemon path for debugging.

## Guardrails

- Keep the flow local-first and approval-first.
- Do not expose secrets in responses.
- Do not run production Board calls unless the user explicitly configured them.
- Prefer `wily agent dev --once --offline-ok` for smoke checks.

## Response Style

- Use Korean when the user is speaking Korean.
- Report concise status and the next action.
- Mention launchd and foreground paths when explaining installation.
