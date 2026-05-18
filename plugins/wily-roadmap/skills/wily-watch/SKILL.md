---
name: wily-watch
description: Use when the user types $wily-watch for a continuously refreshing Wily v3 project pane.
---

# Wily Watch

Render a live task snapshot, including actor lane, blocker text, and cp progress. Tasks are grouped by status (IN_PROGRESS → BLOCKED → READY → DONE) for scannable hierarchy.

## Internal Command

```bash
python3 <plugin-root>/scripts/wily.py watch [--once|--here|--interval N] [--ui auto|rich|ascii] [--compact] [--show-timeline] [--hide-log]
```

## Behavior

- Read-only: does not mutate `.wily/`.
- `--once` prints one snapshot and exits.
- In tmux, `wily watch` opens a right-side pane and runs the live view there.
- `--here` runs the live view in the current terminal.
- `--ui auto` uses Rich styling when available, including repo-local `.venv-watch`; `--ui ascii` forces plain ASCII.
- `--compact` forces single-column compact layout even in wide terminals.
- `--show-timeline` expands checkpoint bars into named checkpoint timelines (e.g. `plan › design › [verify] › deploy`).
- `--hide-log` suppresses the observed commits log panel.
- In a terminal wider than 120 cols, the watch pane shows a Tasks (left) + Activity (right) side-by-side layout.
- Task rows include metadata when space allows: `done` timestamps, `claimed` timestamps, and pending `depends_on` chains.

## Response Style

- Use Korean when the user is speaking Korean.
- Report only the requested roadmap output or concise answer.
- Avoid procedural narration before or after the result.
- Do not echo internal helper commands in normal user-facing responses.
