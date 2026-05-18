# Result

Prerequisite migration/watch-display work is done.

- Migrated this repository's `.wily/roadmap.yaml` to Stage-first schema v14.
- Preserved former roadmap phases as Stage-local child phases in `.wily/stages/**/stage.yaml`.
- Removed legacy external Phase dependencies from Stage-local child Phases; parent Stages now carry cross-Stage dependencies.
- Updated watch rendering so decomposed Stages display their child Phases directly underneath the Stage row.
- Updated watch collapsed summaries so Stage-first roadmaps report done Stages, not Stage nodes plus child phases as a misleading phase count.
- Updated `wily next` so an active Stage-local Phase is reported instead of `Next phase: none`.

The 14-2 smartphone bottom horizontal pane implementation was canceled by user request on 2026-05-15 and should not continue without a later replan.
