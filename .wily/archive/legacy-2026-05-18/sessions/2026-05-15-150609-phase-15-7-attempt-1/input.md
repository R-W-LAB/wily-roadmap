# Wily Phase Context

Phase: 15-7 - Multi-repo onboarding and operating checklist

## Phase

# Phase 15-7: Multi-repo onboarding and operating checklist

## Purpose

Onboard the initial Wily repositories and verify the operational loop from push to sync to board display to PR write action.

## Dependencies

- 15-4 Wily sync webhook, parser, and backfill
- 15-5 GitHub PR writer and phase status toggle
- 15-6 Board UI views, htmx interactions, and mobile layout

## Expected Output

- `wily-roadmap`, `digit`, `mac2win`, and `bounceball` are registered.
- Each repository has the reusable sync workflow and secrets.
- Manual backfill populates the dashboard.
- A test status toggle creates a PR and resyncs after merge.
- Operator checklist documents deploy, logs, resync, and credential rotation.

## Likely Files

- `.github/workflows/wily-board-sync.yml`
- `README.md`
- `deploy/`
- operator notes in the `wily-board` repository

## Known Risks

- Repository and secret changes require explicit user approval.
- Some target repositories may not yet use the current Stage/Phase schema.
- Light's auth path depends on the GitHub account decision.

## Planner Adapter

# Planner

Recommended planner: manual rollout checklist.

Keep remote and secret operations approval-first.

## Prompt

# Execution Prompt

Onboard the initial Wily repositories to Wily Board.

Scope:

- Register target repositories.
- Add or prepare reusable sync workflow files.
- Configure or document required org/repo secrets.
- Run manual backfill.
- Verify dashboard display and one PR-writing action.
- Write concise operating notes for deploy, logs, resync, and credential rotation.

Do not push workflow changes, create secrets, or touch remote repositories without explicit approval.

## Verification

# Verification

Expected checks:

```bash
python3 -m pytest
curl -fsS https://<host>/healthz
```

Live repository checks require approved credentials and should record exact repositories and PR URLs.

## Handoff

# Handoff

Use `docs/wily-board-plan.md`, sections 11 Phase 5, 13, 14, and appendix B.

## Existing Implementation Plan

# Plan

No detailed implementation plan exists yet.
