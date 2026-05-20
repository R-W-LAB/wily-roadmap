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
./wily workspace status
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

## Workspace Manifest

Use `wily workspace` from a parent coordination directory when you want one
read-only view across multiple child Wily repos. The parent file can be
`wily-workspace.yaml` or `.wily-workspace.yaml`.

```yaml
schema: wily-workspace-v1
title: Wily Plugin Workspace
repos:
  - id: wily-roadmap
    path: ./wily-roadmap
  - id: wily-board
    path: ./wily-board
```

The manifest is not a source of truth; each child repo keeps its own
`.wily/tasks.yaml`. `wily workspace init` writes only the manifest and does not create parent `.wily/`.

Useful commands:

```bash
wily workspace init --repo wily-roadmap=./wily-roadmap --repo wily-board=./wily-board --title "Wily Plugin Workspace"
wily workspace show-config --json
wily workspace status --json
wily workspace next
wily workspace watch --once
```

## Wily Agent

The plugin includes the official bundled `wily-agent` daemon for Wily Board v3.
It watches registered `.wily` repositories, builds local-first task snapshots,
and sends best-effort snapshots and heartbeats to Wily Board when local config
is present. As of 2026-05-20, the local `wily-board` repo is deleted for a
fresh rebuild, so Board sync is unavailable until a rebuilt Board URL is
configured.

Typical onboarding:

```bash
wily agent check
wily agent login <one-time-code> --url https://board.example --actor wily
wily agent register --repo OWNER/REPO
wily agent install
wily agent start
wily agent status
```

For foreground smoke tests or development:

```bash
wily agent run --once --offline-ok
```

`wily agent stop` stops the macOS launchd daemon. `wily agent configure --secret`
remains available for legacy signed `/api/live/events` compatibility, but the
Board v3 path uses the token from `wily agent login` after the rebuilt Board
exists. Missing agent config, Board downtime, invalid tokens, or the current
Board rebuild gap are best-effort agent failures; normal Wily task commands
continue to use local `.wily/` state.

`live-*` commands are not a Wily Board v3 reflection mechanism. Stale local
hooks may still call `live-worked --from-hook`; v3 keeps that form as a no-op so
old Codex or Claude hook configuration does not break tool use while you remove
it. Do not re-point stale `live-*` hooks to this moved plugin path.

Custom Workflow does not update Wily checkpoints by itself. Use `wily cp
<task-id> start <cp-name>`, `wily cp <task-id> done <cp-name>`, or `wily cp
<task-id> import-status .wily/handoffs/<task-id>/status.md` to update the local
checkpoint ledger that `wily-agent` includes in snapshots.

## Safety

Wily behavior stays local-first. Remote or destructive work requires explicit
user approval. `wily land` asks before pushing unless the user separately handles
the push.
