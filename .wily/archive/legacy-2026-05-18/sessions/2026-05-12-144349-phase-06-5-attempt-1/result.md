# Result

Implemented completed-stage compaction for long Wily watch panes.

- Updated the collapsed summary to report both completed phase count and completed stage count.
- Adjusted constrained-height trimming to preserve unfinished/current/ready/blocked phase lines ahead of rails and decorative stage headers.
- Updated `wily-watch` guidance with the completed-stage compaction contract.
- Added long-roadmap tests for compacted stage meaning and unfinished phase preservation.
- Saved the detailed implementation plan at `docs/superpowers/plans/2026-05-12-wily-watch-stage-compaction.md`.
