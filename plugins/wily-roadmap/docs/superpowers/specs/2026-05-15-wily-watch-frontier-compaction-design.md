# Wily Watch — Frontier Stage Compaction Design

## Purpose

`$wily-watch` must stay useful in a narrow right-side pane even when a roadmap has dozens of unfinished phases. The current height fallback slices from the bottom when the rendered body is too tall. In a long roadmap like `/Users/wilycastle/Code/projects/digit` (75 phases, 1 done, 74 pending), that means the pane shows late future stages while hiding the next executable work near the top.

This change makes height compaction prioritize the current execution frontier: collapse already-completed leading work, expand the next actionable stage, and summarize later future stages instead of rendering every internal phase.

Scope: watch rendering only. Do not change roadmap DAG semantics, `$wily-next`, phase status calculation, tmux pane creation, mouse event plumbing, or the existing left-click completed-stage toggle.

## Observed Problem

The digit roadmap is large enough to reproduce the failure:

- `stage_groups()` yields 17 dependency stages.
- Stage 1 is done.
- Stages 2 through 17 are pending, with Stage 2 containing the next frontier work.
- With small pane heights, the current `_body_lines()` fallback returns `lines[-max_rows:]`.

The resulting watch pane can show only late stages such as Stage 15-17. That is backwards for a roadmap dashboard: the user needs the next runnable or earliest pending stage first, with later stages folded into compact summaries.

## Definitions

- **Done prefix:** the leading run of stages where every phase is `done`.
- **Frontier stage:** the earliest stage after the done prefix that contains a ready phase from `view.ready_ids`. If no ready phase exists, it is the earliest stage after the done prefix that contains any non-done phase.
- **Future stage:** any stage after the frontier stage.
- **Future stage summary:** a single compact row for a future stage, e.g. `Stage 3 - 9 phases pending`.

`done`, `superseded`, and other non-pending statuses inside future stages still count toward the stage summary. The row should prefer a clear pending count because the overflow problem is unfinished work volume.

## Rendering Behavior

When the full graph or flat body fits in the available rows, render the existing full view unchanged.

When it does not fit:

1. Collapse the done prefix using the existing completed-work summary behavior unless `expand_done=True`.
2. Identify the frontier stage.
3. Render the frontier stage header and all phase rows in that stage.
4. Render later future stages as one summary row per stage.
5. If the compact body is still too tall, preserve the done summary and frontier stage first, then trim the future summary rows from the bottom.

The renderer must not fall back to tail-slicing unfinished work. If only one or two body rows are available, the rows should still favor the frontier stage over late future stages.

## Interaction

No new mouse binding is added in this phase.

Existing interactions remain:

- Left click and `d` toggle completed work between collapsed and expanded states.
- When completed work is expanded, mouse wheel scrolling continues to move through the expanded body.
- Right click continues to pass through to the user's tmux context menu behavior.

Future stage summaries are display-only for this change. A later phase may add click or key expansion for an individual future stage, but that is intentionally out of scope here.

## Implementation Notes

The compaction should be stage-aware, not line-slice based.

Expected structure:

- Add a small internal representation for stage render groups, or derive equivalent grouped line blocks from `_ordered_stages()`.
- Reuse `_stage_header()` and `_node_line()` for frontier rows so the compact view looks like the existing flat fallback.
- Reuse existing done-prefix summary line where possible.
- Apply the new compaction in `_body_lines()` only after the normal full render fails to fit.
- Keep graph rendering for roadmaps that fit. For constrained long roadmaps, it is acceptable for the compacted form to use the flat stage view because summary rows are stage-level, not rail-level.

The key invariant is that constrained output should be based on semantic stage groups:

```text
done prefix summary
frontier stage expanded
future stage summaries
```

not on the last N rendered lines.

## Testing

Add focused tests in `tests/test_wily_watch_ui.py` with a long roadmap fixture shaped like the digit project:

- A leading done Stage 1.
- A large Stage 2 containing ready or earliest pending phases.
- Several later pending stages with enough total rows to exceed small pane heights.

Assertions:

- A constrained render includes Stage 2 or its first phase id/title.
- The same constrained render does not show only late tail stages.
- Future stage summary rows appear, such as `Stage 3 - 9 phases pending`.
- Very small `max_rows` still favors the frontier over late future stages.
- `expand_done=True` keeps the existing expanded-done scroll behavior intact.
- Existing tests for right-click footer text and left-click/d toggle behavior continue to pass.

Verification command:

```bash
python3 -m unittest discover
```

Also run:

```bash
python3 -m py_compile scripts/wily.py scripts/wily_state_summary.py scripts/wily_watch_ui.py scripts/wily_runner.py
git diff --check
```

## Non-Goals

- No interactive expansion of future stage summaries yet.
- No changes to `$wily-next` or executable phase selection.
- No changes to tmux split behavior, tmux popup/context-menu handling, or right-click pass-through.
- No changes to `.wily/roadmap.yaml` schema.
- No new CLI flags.
