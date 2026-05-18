# Wily Roadmap

Wily is a local-first roadmap workflow plugin for agentic coding sessions.

## Install and Update

For first-time sharing, Wily can be sent as a zip bootstrap package. A zip install works locally, but it cannot pull future updates in place because it has no git metadata.

After installing a bootstrap zip, migrate once to a managed GitHub install:

```bash
./wily update --migrate
```

The migration creates a sibling `wily-roadmap-managed` directory and leaves the original zip directory unchanged.

For an install that is already git-managed, check for updates with:

```bash
./wily update --check
```

Apply an available update only when the working tree is clean:

```bash
./wily update --yes
```

Updates are explicit and approval-first. Wily does not check for updates in the background, does not patch zip installs in place, and only applies fast-forward git updates.

## Repo-Local Zsh Command

From the plugin root, run Wily with the checked-in zsh launcher:

```bash
./wily status
./wily next
./wily migrate-state --to wily-roadmap-v2 --dry-run
./wily run <stage-id>/<phase-id> --dry-run
./wily watch
./wily watch --once --ui ascii
./wily update --check
```

`./wily watch` is the live roadmap dashboard. Inside tmux it opens a right-side split pane and targets the current `TMUX_PANE` when tmux exposes it. Outside tmux, including when working beside Codex app, run it in a side terminal and it will use that terminal directly.

## Stage/Phase v2

`wily-roadmap-v2` is the durable roadmap model. `.wily/roadmap.yaml` stores Stage rows, and `.wily/stages/<stage-id>-<slug>/stage.yaml` stores child Phases. Stage is the collaboration and aggregation boundary; Phase is the execution unit.

Use canonical Phase refs for v2 execution:

```bash
./wily start <stage-id>/<phase-id>
./wily run <stage-id>/<phase-id> --dry-run
./wily checkpoint-sync <stage-id>/<phase-id> --status-board agent-handoffs/example-status.md
./wily complete <stage-id>/<phase-id>
```

Stage ids are not executable. If a repository still has legacy top-level `phases:`, inspect the migration first:

```bash
./wily migrate-state --to wily-roadmap-v2 --dry-run
```

`--apply` writes a backup and migration report. Legacy cleanup requires the explicit `--prune-legacy` mode.

For the styled Rich dashboard, install the optional watch UI dependency once:

```bash
./wily watch --install-ui
```

The launcher delegates to `scripts/wily.py` and keeps the current working directory as the target repository. It does not modify shell startup files, install aliases, touch PATH, contact remotes, or perform destructive actions by itself.

Use `python3 scripts/wily.py <command>` when a Python-only invocation is preferred.

Wily behavior stays local-first: remote or destructive work requires explicit user approval.
