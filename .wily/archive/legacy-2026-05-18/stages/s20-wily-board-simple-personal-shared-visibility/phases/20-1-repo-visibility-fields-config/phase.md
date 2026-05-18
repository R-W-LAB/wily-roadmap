# Phase 20-1: Repo visibility fields and config contract

## Purpose

Add simple repo visibility fields and a config contract for personal repositories.

## Acceptance

- `repos` stores `visibility` with default `shared`.
- `repos` stores optional `visible_to`.
- Existing registered repositories remain shared by default.
- Personal repo config can map repo full names to a login, such as `airmang/solo-tool:airmang`.
