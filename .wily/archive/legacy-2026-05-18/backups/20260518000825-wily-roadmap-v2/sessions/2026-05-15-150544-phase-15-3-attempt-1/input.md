# Wily Phase Context

Phase: 15-3 - FastAPI auth and SQLite skeleton

## Phase

# Phase 15-3: FastAPI auth and SQLite skeleton

## Purpose

Build the backend foundation: FastAPI routes, SQLite schema, GitHub OAuth, whitelist sessions, health checks, and empty HTML pages.

## Dependencies

- 15-1 Wily Board repository and contract baseline

## Expected Output

- FastAPI app starts locally with `/healthz`.
- SQLite schema includes repos, stages, phases, events, and oauth_sessions.
- GitHub OAuth callback can be tested with mocks.
- Unauthorized users are rejected after OAuth if not in the whitelist.
- Initial HTML routes return 200 with empty states.

## Likely Files

- `app/main.py`
- `app/config.py`
- `app/auth/`
- `app/db/schema.sql`
- `app/db/repo.py`
- `app/web/routes.py`
- `tests/test_auth.py`
- `tests/test_schema.py`

## Known Risks

- OAuth implementation needs careful redirect URI and cookie security handling.
- Storing sessions in SQLite is sufficient for two users, but expiry cleanup must exist.

## Planner Adapter

# Planner

Recommended planner: superpowers:test-driven-development

Start with schema and auth tests before route implementation.

## Prompt

# Execution Prompt

Implement the Wily Board backend skeleton.

Scope:

- Add FastAPI app setup, config loading, SQLite schema and repository helpers.
- Add `/healthz`, `/`, `/repos/{owner}/{name}`, and auth start/callback routes.
- Implement GitHub OAuth and whitelist session logic with testable seams.
- Add tests for schema creation, webhook signature helper if introduced, and OAuth callback behavior using mocks.

Do not implement sync ingestion or PR-writing in this phase.

## Verification

# Verification

Expected checks:

```bash
python3 -m pytest tests/test_auth.py tests/test_schema.py
python3 -m py_compile app/main.py app/config.py
```

Adjust commands to the final project tooling.

## Handoff

# Handoff

Use `docs/wily-board-plan.md`, sections 5 through 7 and appendix A.

## Existing Implementation Plan

# Plan

No detailed implementation plan exists yet.
