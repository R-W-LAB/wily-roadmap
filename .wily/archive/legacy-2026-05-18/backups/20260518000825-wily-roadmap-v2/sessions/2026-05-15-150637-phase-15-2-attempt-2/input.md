# Wily Phase Context

Phase: 15-2 - Azure box bootstrap artifacts

## Phase

# Phase 15-2: Azure box bootstrap artifacts

## Purpose

Prepare deployment artifacts for a lightweight Ubuntu 24.04 Azure VM running Caddy, FastAPI, SQLite, and systemd without Docker.

## Dependencies

- 15-1 Wily Board repository and contract baseline

## Expected Output

- `deploy/install.sh` provisions non-root execution, SSH hardening assumptions, ufw, fail2ban, swap, Python 3.12, uv, Caddy, and app directories.
- `deploy/Caddyfile` exposes HTTPS for the chosen host and supports rate limits where available.
- `deploy/wily-board.service` runs uvicorn with one worker.
- The deployment path avoids Docker and stays within the 1 GiB memory budget.

## Likely Files

- `deploy/install.sh`
- `deploy/Caddyfile`
- `deploy/wily-board.service`

## Known Risks

- Caddy `rate_limit` requires a build/module decision; if unavailable, keep rate limiting in the app or document the operational gap.
- Hostname, SSH, and secret values are user-owned and must not be guessed.

## Planner Adapter

# Planner

Recommended planner: manual Codex implementation.

Use conservative shell scripts with explicit prerequisites and dry-run-friendly comments.

## Prompt

# Execution Prompt

Implement Azure VM bootstrap artifacts for Wily Board.

Scope:

- Add deploy scripts and service files for Ubuntu 24.04, Caddy, Python 3.12, uv, systemd, SQLite storage, ufw, fail2ban, and 1 GiB swap.
- Keep values configurable via environment files.
- Do not use Docker.
- Do not connect to Azure, alter the real server, or register DNS without explicit approval.

## Verification

# Verification

Expected checks:

```bash
sh -n deploy/install.sh
systemd-analyze verify deploy/wily-board.service
caddy validate --config deploy/Caddyfile
```

Run available checks locally and document any host-only checks that cannot run.

## Handoff

# Handoff

Use `docs/wily-board-plan.md`, sections 4, 7, 11 Phase 1, and appendix A.

## Existing Implementation Plan

# Plan

No detailed implementation plan exists yet.
