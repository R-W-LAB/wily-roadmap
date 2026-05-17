# Board Operations

This reference is the Wily plugin-side operations checklist for reflecting local `.wily` changes on Wily Board.

## End-to-End Procedure

1. Make the local `.wily` state change first. Keep `.wily` as the durable source of truth.
2. Check live config with the relevant Wily helper or `wily board check --probe`. Live config may come from user config, `.wily/board.json`, `.wily/local/board.json`, or `WILY_BOARD_*` environment values.
   Operators must check live config before network reflection.
3. Emit or replay the Board projection:
   The normal operation is to emit or replay the best available projection.
   - lifecycle/session changes emit the corresponding live event;
   - runner checkpoint overlays use `wily.py checkpoint-sync <phase-id> --status-board <path>`;
   - local Stage decomposition drafts use `wily.py board sync-local <stage-id>` and `stage_decomposed_local`.
4. Verify with deterministic evidence first: emit result cache, API response, SSE event, or SSR HTML.
5. Use actual-site visual verification only when deterministic verification fails, reports a mismatch, UI/rendering changed, or the user explicitly asks for visual confirmation.

## Actual-Site Visual Verification

The production site is:

```text
https://rnwlab.duckdns.org
```

Use Chrome with the user's logged-in session first. If Chrome/browser automation cannot access the site, request explicit user approval before creating a temporary verification session. Then clean up and delete any temporary verification session after the check, and record cleanup in the handoff or response.

## Failure Response

When reflection fails, preserve the local Wily state and surface recovery:

- name the changed Wily state;
- name the failed Board event or projection;
- provide `wily board check --probe` or `wily board sync-local <stage-id>`;
- say actual-site visual verification remains incomplete when it has not been performed.

Board outages do not roll back or block local Wily state transitions.
