# Result

Implemented runner artifact archive finalization and review handoff support.

- Preserved unknown session status blocks, including `runner:`, when `wily complete` and `wily block` rewrite session status.
- Added final runner artifact snapshot behavior for `wily complete` and `wily block`.
- Added `runner_archive:` metadata and `runner/archive-summary.md` for finalized runner sessions.
- Added `review-handoff.md` generation in both `agent-handoffs/` and `.wily/sessions/<session>/runner/`.
- Updated `wily-run` and `wily-complete` skill guidance to match the implemented archive lifecycle.
- Synced updated runtime and skill files into the local Codex plugin cache.
