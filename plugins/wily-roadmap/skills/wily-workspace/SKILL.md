---
name: wily-workspace
description: Use when the user asks for $wily-workspace or wants manifest-only multi-repo Wily status from a parent coordination directory.
---

# Wily Workspace

Show or create a parent workspace manifest for multiple child Wily repos.

## Internal Command

```bash
python3 <plugin-root>/scripts/wily.py workspace <init|show-config|status|next|watch> [args]
```

## Behavior

- The manifest can be `wily-workspace.yaml` or `.wily-workspace.yaml`.
- The manifest is not a source of truth; each child repo keeps its own `.wily/tasks.yaml`.
- `wily workspace init` writes only the manifest and does not create parent `.wily/`.
- `wily workspace status` shows per-repo progress, active tasks, ready tasks, blocked tasks, and per-repo errors.
- `wily workspace next` aggregates ready tasks without claiming them.
- `wily workspace watch --once` prints one aggregate snapshot; without `--once`, it redraws when child `.wily/.touch` files change.
- Missing or invalid child repos should be reported as per-repo errors, not as a reason to create parent Wily state.

## Response Style

- Use Korean when the user is speaking Korean.
- Report only the requested workspace output or concise answer.
- Avoid implying that the parent manifest owns task status.
- Do not echo internal helper commands in normal user-facing responses.
