# Board Reflection Contract

This contract applies to Wily commands that mutate roadmap, Stage, Phase, session, revision, or live projection state.

Durable `.wily` state remains authoritative. Board is a live/provisional projection for collaboration visibility and must not become the source of truth.

## State-Changing Procedure

1. Apply the local `.wily` state change first.
2. Check Board live config from user config, repo-local `.wily/board.json`, repo-local `.wily/local/board.json`, or `WILY_BOARD_*` environment values.
   Always check Board live config before attempting live reflection.
3. When live config is available, emit or replay the related Board live/provisional projection:
   - lifecycle status changes use the matching live event such as `start`, `complete`, `block`, or `release`;
   - Custom Workflow status boards use `wily.py checkpoint-sync <stage-id>/<phase-id> --status-board <path>`;
   - Stage decomposition topology uses `stage_decomposed_local` and can be replayed with `wily.py board sync-local <stage-id>`.
4. Verify Board reflection with deterministic evidence such as an emit result, API response, SSE event, or SSR HTML.
5. Include compact Board evidence for important transitions such as `$wily-run`, `$wily-complete`, `$wily-block`, and `$wily-replan`.

## Actual-Site Visual Verification

Routine success does not require browser visual verification. Actual-site visual verification of the actual production Board site at `https://rnwlab.duckdns.org` is mandatory when:

- deterministic Board verification fails;
- deterministic evidence reports a mismatch with `.wily` state;
- the user explicitly asks for visual confirmation;
- the implementation changes Board UI/rendering behavior.

Use the user's Chrome logged-in session first. If Chrome or browser automation is unavailable, stop and request explicit user approval before creating a temporary verification session. After a temporary verification session is used, delete it and record cleanup.

## Failure Handling

Board reflection failure must not roll back, undo, or block the underlying local Wily state change. The user response should warn clearly and include:

- what Wily state changed;
- which Board event or projection failed;
- the recovery command, for example `wily board check --probe` or `wily board sync-local <stage-id>`;
- whether actual-site visual verification remains incomplete.

Recovery should prefer deterministic checks first:

```bash
wily board check --probe
wily board sync-local <stage-id>
```

After deterministic recovery, use actual-site visual verification only under the escalation rules above.

## Command Scope

The contract applies to at least:

- `$wily-init`
- `$wily-start`
- `$wily-run`
- `$wily-decompose-stage`
- `$wily-complete`
- `$wily-block`
- `$wily-retry`
- `$wily-replan`
- `$wily-issues --add-to-roadmap` after explicit approval
- any future Wily command that mutates `.wily` roadmap, Stage, Phase, session, revision, or live projection state

Read-only commands such as `$wily-status`, `$wily-next`, and `$wily-watch` do not emit Board updates merely because they read local state.
