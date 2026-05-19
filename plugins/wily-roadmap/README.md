# Wily Roadmap

Wily Roadmap v3 is a local-first Project + flat goal-sized Task manager for
agentic coding sessions.

## Commands

From the plugin root:

```bash
./wily status
./wily next
./wily claim T01
./wily go T01
./wily done T01
./wily watch --once
./wily agent check
```

The launcher delegates to `scripts/wily.py` and keeps the current working
directory as the target repository. It does not modify shell startup files,
install aliases, touch PATH, contact remotes, or perform destructive actions by
itself.

## State

Wily v3 stores durable project state under `.wily/`:

- `project.md`
- `tasks.yaml`
- `actors.yaml`
- `tasks/<id>/progress.jsonl`
- `tasks/<id>/result.md`
- `archive/` for legacy snapshots

`wily init commit` also creates or updates concise Wily guidance in root
`AGENTS.md` and `CLAUDE.md`, preserving existing project-specific instructions.

## Custom Workflow

`wily go <id>` prints goal text for
`custom-workflow-skillset:plan-goal-runner`. Wily does not invoke external
runners directly.

## Wily Agent

The plugin includes a bundled `wily-agent` daemon for optional local heartbeat
events. It watches registered `.wily` repositories and sends signed best-effort
live events to Wily Board when local config is present.

Typical onboarding:

```bash
wily agent check
wily agent configure --url https://board.example --repo OWNER/REPO --actor wily --secret "$WILY_BOARD_SECRET"
wily agent register --repo OWNER/REPO
wily agent install
wily agent start
wily agent status
```

For foreground smoke tests or development:

```bash
wily agent dev --once --offline-ok
```

`wily agent stop` stops the macOS launchd daemon. Missing agent config, Board
downtime, and invalid secrets are best-effort agent failures; normal Wily task
commands continue to use local `.wily/` state.

## Safety

Wily behavior stays local-first. Remote or destructive work requires explicit
user approval. `wily land` asks before pushing unless the user separately handles
the push.
