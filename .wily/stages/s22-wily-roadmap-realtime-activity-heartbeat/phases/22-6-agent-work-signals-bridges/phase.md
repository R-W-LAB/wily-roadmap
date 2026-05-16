# Phase 22-6: Agent work signals and bridges

## Purpose

Emit token-zero `worked` events for Codex and Claude activity.

## Acceptance

- Claude and Codex hooks resolve active sessions from `.wily/local/live/active/*.json`.
- Codex Desktop App Server bridge converts tool-completion events into `worked`.
- Missing bridge or hook failures degrade to heartbeat-only activity.
- The model never has to spend tokens calling `wily live-worked`.
