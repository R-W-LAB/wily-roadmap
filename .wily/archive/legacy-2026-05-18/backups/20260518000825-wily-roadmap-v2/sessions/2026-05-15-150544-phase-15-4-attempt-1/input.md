# Wily Phase Context

Phase: 15-4 - Wily sync webhook, parser, and backfill

## Phase

# Phase 15-4: Wily sync webhook, parser, and backfill

## Purpose

Ingest `.wily/` state from GitHub into Wily Board's SQLite cache through signed webhooks and manual backfill.

## Dependencies

- 15-3 FastAPI auth and SQLite skeleton

## Expected Output

- `/webhooks/github` verifies HMAC signatures and accepted repositories.
- GitHub contents or archive fetch retrieves `.wily/roadmap.yaml` and `.wily/stages/**/stage.yaml`.
- Parser maps Stage and Phase state into SQLite upserts.
- `/admin/repos/{owner}/{name}/resync` can rebuild cache from default branch.
- Events record sync and backfill actions.

## Likely Files

- `app/sync/webhook.py`
- `app/sync/pull.py`
- `app/sync/parser.py`
- `app/db/repo.py`
- `app/web/routes.py`
- `.github/workflows/wily-board-sync.yml`
- `tests/test_parser.py`
- `tests/test_webhook_signature.py`

## Known Risks

- Importing parser code directly from `wily-roadmap` may create packaging friction across repositories.
- YAML parsing must preserve the current Stage/Phase schema but can stay read-only in this phase.
- Webhook replay and unknown repo handling need explicit behavior.

## Planner Adapter

# Planner

Recommended planner: superpowers:test-driven-development

Use fixture `.wily/roadmap.yaml` and `stage.yaml` files from this repository to drive parser tests.

## Prompt

# Execution Prompt

Implement Wily Board sync ingestion.

Scope:

- Verify webhook HMAC signatures.
- Fetch `.wily/` files from GitHub for a pushed SHA or manual resync target.
- Parse roadmap and stage YAML into repos, stages, phases, and events.
- Add a reusable workflow template for Wily repositories to notify the board.
- Prove the parser can ingest the current `wily-roadmap` Stage/Phase files.

Do not implement dashboard write actions in this phase.

## Verification

# Verification

Expected checks:

```bash
python3 -m pytest tests/test_parser.py tests/test_webhook_signature.py
python3 -m py_compile app/sync/webhook.py app/sync/pull.py app/sync/parser.py
```

Add an integration fixture using this repository's `.wily/roadmap.yaml` and one `stage.yaml`.

## Handoff

# Handoff

Use `docs/wily-board-plan.md`, sections 2, 3, 6, 8, and 11 Phase 3.

## Existing Implementation Plan

# Plan

No detailed implementation plan exists yet.
