# Phase 23-4: Durable sync draft reconciliation

## Purpose

Clear provisional topology once durable GitHub sync imports matching child phases.

## Scope

- Clear drafts by repository and Stage.
- Keep cleared rows for audit by setting `cleared_at`.
- Avoid clearing unrelated drafts.
