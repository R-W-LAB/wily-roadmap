# Verification

Verify Stage s23 with:

- Wily CLI unit tests for `decompose-stage` draft event emission and missing-config diagnostics.
- Board live event API tests for valid and invalid `stage_decomposed_local` payloads.
- Board DB tests for `live_drafts` storage, listing, and durable sync clearing.
- Board web route tests for provisional child Phase rendering and dashboard follow-up rows.
- Full Wily Roadmap CLI test suite.
- Full Wily Board pytest suite.

Manual smoke:

1. Configure `.wily/local/board.json` locally.
2. Decompose a pending Stage locally.
3. Confirm Board shows draft child Phases before commit and push.
4. Commit and push `.wily` changes.
5. Confirm Board replaces draft rows with durable rows after sync.
