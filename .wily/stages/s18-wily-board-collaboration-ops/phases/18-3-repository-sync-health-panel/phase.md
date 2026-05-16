# Phase 18-3: Repository sync health panel

## Purpose

Show whether each registered repository is syncing correctly.

## Acceptance

- Board shows last sync time, initialized/missing `.wily` state, and webhook freshness.
- Registered repos with no `.wily/roadmap.yaml` are clearly marked as not initialized.
- Health panel stays read-only.
