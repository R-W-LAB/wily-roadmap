# Wily Roadmap v2 Stage/Phase Contract

This contract is the execution baseline for S27.

## Identity

- Durable schema name: `wily-roadmap-v2`.
- `.wily/roadmap.yaml` stores Stage rows only.
- `.wily/stages/<stage-id>-<slug>/stage.yaml` stores child Phase rows.
- `.wily/phases/**` is legacy input or archive after migration.
- Canonical Phase identity is `(stage_id, phase_id)`.
- User-facing Phase references use `<stage-id>/<phase-id>`, for example `s27/p04`.
- New Stage-local Phase ids should be short within the Stage, for example `p01`, `p02`, `p03`.

## Execution Boundary

Stage is never executable. Stage is the large flow, collaboration boundary, dependency boundary, and progress/risk aggregate.

Phase is the only execution unit. These commands must resolve a Phase identity:

- `wily start <stage-id>/<phase-id>`
- `wily run <stage-id>/<phase-id>`
- `wily complete <stage-id>/<phase-id>`
- `wily block <stage-id>/<phase-id> [reason]`
- `wily retry <stage-id>/<phase-id>`
- `wily release <stage-id>/<phase-id>`
- `wily live-heartbeat <stage-id>/<phase-id>`
- `wily live-worked <stage-id>/<phase-id>`
- `wily checkpoint-sync <stage-id>/<phase-id> --status-board <path>`

If a user passes a Stage id to a Phase-only command, the command must fail without creating a Phase. The message should suggest the nearest ready Phase when known, or `wily decompose-stage <stage-id>` / `wily migrate-state --to wily-roadmap-v2 --dry-run` when the Stage has no executable Phase.

## Stage Aggregate Status

Stage display status is derived from child Phase status and Stage dependencies. Commands may write a normalized Stage `status` for compatibility, but v2 logic must be able to recompute it.

Aggregate precedence:

1. `superseded`: explicit Stage terminal override.
2. `done`: every non-superseded child Phase is `done`.
3. `in_progress`: at least one child Phase is `in_progress`.
4. `blocked`: no Phase is `in_progress` and at least one child Phase is `blocked`.
5. `needs_review`: no Phase is `in_progress` or `blocked` and at least one child Phase is `needs_review`.
6. `ready`: Stage dependencies are done and at least one child Phase is executable.
7. `pending`: dependencies are not done or no child Phase is executable.

A non-superseded Stage with zero child Phases is invalid for execution. Read-only commands may display it with a warning.

## Migration Defaults

S27 resolves the design-spec open questions with these defaults:

- Direct Stage conversion title: preserve the Stage title exactly for the generated `p01` Phase. Do not add an implementation suffix.
- Root Board route: `/` redirects to `/me`. The app may remember a user's last surface later, but S27 keeps the redirect deterministic.
- Board stale threshold: live activity becomes stale after 15 minutes without heartbeat. A repo card can show old activity context beyond that, but the live chip is stale.
- Backup retention: backups are retained indefinitely by default. Cleanup is manual and approval-first.

`wily migrate-state --to wily-roadmap-v2 --dry-run` must not mutate durable state. `--apply` writes backup and reports before modifying state. `--prune-legacy` is the only mode that can remove legacy `.wily/phases/**` files.

## Custom Workflow Adapter

Custom Workflow Skillset is an external black-box runner. Wily may read and route to its artifacts, but must not edit or require changes inside the plugin.

Custom Workflow status-board checkpoints are non-durable child rows under the owning Wily Phase:

- `is_durable: false`
- source is `custom-workflow`
- rows attach under `(repo, stage_id, phase_id)`
- checkpoint completion never marks the Wily Phase `done`

Final Phase transition remains a Wily lifecycle action after verification evidence exists.

## Projection

Watch, status, and Board emitters consume the same projection semantics:

- schema: `wily-roadmap-projection-v1`
- input: durable Stage/Phase YAML, sessions, live overlays, Custom Workflow status boards, and Board emit cache
- output: repo metadata, Stage rows, Phase rows, checkpoint overlays, live overlays, and warnings

Wily Board is read-only for roadmap state. It may render and store imported/signed projection data, but `.wily` remains the source of truth.
