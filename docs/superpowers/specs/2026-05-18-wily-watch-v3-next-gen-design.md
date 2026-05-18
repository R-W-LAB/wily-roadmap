# Wily Watch V3 Next-Gen UI Design

## Motivation

The current `wily watch` UI (restored in v3 from v2) renders tasks as a flat, chronologically-ordered list with basic checkpoint bars and blocker notes. While functional, it does not exploit the full expressiveness of the v3 flat-task data model. Tasks have status, assignee, actor, checkpoint history, blockers, dependencies, and observed commits. A next-generation watch UI should surface these dimensions as a cohesive, information-dense, and visually scannable dashboard.

## Design Principles

1. **Information Density First** – Every row must answer: *what is the state of this task and who owns it?*
2. **Visual Hierarchy by Status** – DONE, IN_PROGRESS, READY, BLOCKED are not just labels; they are spatial groupings.
3. **Temporal Awareness** – Checkpoint start/done timestamps, last observed commit, and actor activity give a sense of *liveness*.
4. **Responsive to Pane Size** – The watch runs mostly inside a tmux split; the layout must gracefully degrade from 132 cols to 72 cols.
5. **Terminal-Native** – No curses, no mouse, no TUI frameworks. Pure Rich/ASCII print loops for maximum compatibility.

## Layout Architecture

The screen is divided into five conceptual panels rendered top-to-bottom in standard mode, and side-by-side in wide mode.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Wily Roadmap v3  Project Title                              v3.0.1   mode    │  Header
├─────────────────────────────────────────────────────────────────────────────┤
│  ████████████████████████████████░░░░░░░  12/20 · 60%   3 blocked  2 active │  Summary
├─────────────────────────────────────────────────────────────────────────────┤
│ TASKS                                    │ ACTIVITY                         │
│ ├─ ● T01  done      wily   Title A       │ wily    T03 (verify)   2m ago    │
│ │   cp [████████░░░] 4/5 cp current:test│ right   T02 (plan)     15m ago   │
│ ├─ ◐ T02  in_prog  right  Title B       │                                  │
│ │   cp [████░░░░░░░] 2/5 cp current:plan │                                  │
│ ├─ ▶ T03  ready     wily   Title C       │                                  │
│ ├─ ✗ T04  blocked   —     Title D       │                                  │
│ │   blocker: waiting for API key          │                                  │
│ └─ ✗ T05  blocked   wily   Title E       │                                  │
│     blocker: dependency T04               │                                  │
│                                          │                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ OBSERVED  3 commits since fork                                           │  Log
│ ⏵ abc123  wily   "refactor: extract parser"  → guessed T03                 │
│ ⏵ def456  right  "fix: handle null input"    → no scope match             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Panel Definitions

| Panel | Standard | Wide | Compact | Purpose |
|-------|----------|------|---------|---------|
| **Header** | full width | full width | single line | Project title, version, mode |
| **Summary** | full width | full width | 2 lines | Progress bar, KPI counts |
| **Tasks** | full width | left 60% | full width | Grouped task list with detail rows |
| **Activity** | hidden | right 40% | hidden | Per-actor current task + last action |
| **Log** | full width | full width | last 2 lines | Observed commits (collapsible) |

### Responsive Breakpoints

- **Compact (< 80 cols)** – Single column, minimal glyphs (`* ~ > x`), truncated titles, no activity panel, log hidden unless `--show-log`.
- **Standard (80–119 cols)** – Full layout, 60/40 split for tasks/log (log below tasks), actor summary line only.
- **Wide (>= 120 cols)** – Tasks (left) + Activity (right) side-by-side, log below in full width, checkpoint timeline visible.

## Task List Panel

### Status Grouping

Tasks are **not** rendered in input order. They are grouped by status priority:

1. **IN_PROGRESS** – Most important; always at the top.
2. **BLOCKED** – Needs attention; second priority.
3. **READY** – Available to pick up.
4. **DONE** – Collapsed by default in compact mode, shown last.

Each group has a subtle header line:

```
── IN PROGRESS ──────────────────────────────────────
```

### Task Row Anatomy

A task row is a single primary line followed by zero or more detail child lines.

**Primary Line:**

```
├─ ◐ T02  in_progress  right  Title B               [depends: T01]
```

Columns (fixed-width where possible):

| Glyph | ID | Status | Actor | Title | Meta |
|-------|-----|--------|-------|-------|------|
| `◐` | `T02` | `in_progress` | `right` | `Title B` | `[depends: T01]` |

- **Glyph** – 2 chars, colored by status.
- **ID** – 5 chars, left-aligned.
- **Status** – 12 chars, left-aligned, colored.
- **Actor** – 10 chars, left-aligned, dim if unassigned.
- **Title** – Flexible, truncated with `…` if too long.
- **Meta** – Right-aligned; shows `depends: Txx`, `claimed 5m ago`, or `done 1h ago`.

**Detail Child Lines:**

- **Checkpoint Bar** – Only when `cp_summary.total > 0`.
  ```
  │   cp [████████░░░] 4/5 cp current:test
  ```
  In wide mode, append a mini-timeline of checkpoint names:
  ```
  │   cp [████████░░░] 4/5  plan > design > test > verify > deploy
  ```
  Completed checkpoints are dim, current is bold, remaining are hidden or dim.

- **Blocker** – Only when `task.blocker` is set.
  ```
  │   blocker: waiting for API key
  ```
  In rich mode, the entire line is red. In ASCII, prefixed with `!`.

- **Dependency Chain** – When `task.depends_on` exists and dependencies are not DONE.
  ```
  │   waiting for: T01 (in_progress), T04 (blocked)
  ```

### Color & Style Map (Rich Mode)

| Element | Style | Rationale |
|---------|-------|-----------|
| IN_PROGRESS glyph | `bold yellow` | Attention |
| BLOCKED glyph | `bold red` | Urgent |
| READY glyph | `bold cyan` | Actionable |
| DONE glyph | `green dim` | Completed, de-emphasized |
| Checkpoint bar fill | `green` | Progress is good |
| Checkpoint bar empty | `dim` | Not yet started |
| Blocker text | `red` | Problem state |
| Actor name | `bold` if active, `dim` if idle | Ownership clarity |
| Observed commit | `dim` | Secondary information |
| Group header rule | `dim` | Structural separation |

## Actor Activity Panel (Wide Mode Only)

A side panel that answers: *who is working on what, and when did they last act?*

```
ACTIVITY
────────────────────────────
wily
  current: T03 verify      2m ago
  last done: T01             1h ago
  pace: 1.2 tasks/hour

right
  current: T02 plan         15m ago
  idle since: —
```

Columns:
- **Actor ID** – bold.
- **Current Task** – Task ID + current checkpoint, timestamp since last event.
- **Last Done** – Most recently completed task + timestamp.
- **Pace** – (Optional) tasks completed per hour based on `done_at` timestamps.

Data sources:
- `task.actor` + `task.status == IN_PROGRESS` → current task.
- `progress.jsonl` last event → last action timestamp.
- `task.done_at` → last completed task.

## Checkpoint Timeline (Wide Mode Opt-In)

When `--show-timeline` is passed, the checkpoint bar expands into a named timeline:

```
│   cp [██████░░░░] 3/5  analysis > design > implement > test > deploy
                              ↑ current
```

- Completed checkpoints: `dim` + strikethrough (Rich) or `[]` brackets (ASCII).
- Current checkpoint: `bold` + `↑` indicator.
- Future checkpoints: hidden in compact, `dim` in standard/wide.

## Observed Commits Log

The log panel remains at the bottom but gains a collapsible behavior:
- `--show-log` (default in standard/wide): shows last N commits.
- `--hide-log`: suppresses entirely.
- In compact mode: only shows count, e.g., `3 observed commits`.

Each log entry now includes a **scope match score**:
```
⏵ abc123  wily   "refactor: extract parser"  → T03  (scope: 2 files match)
```

## Interaction Model

Watch is a *read-only* display; however, we can support **keyboard-driven mode switching** when `--interactive` is passed (outside tmux pane):

| Key | Action |
|-----|--------|
| `c` | Toggle compact mode |
| `t` | Toggle checkpoint timeline |
| `l` | Toggle observed log |
| `a` | Toggle activity panel (wide only) |
| `q` | Quit watch loop |

These are soft toggles that adjust the `WatchLayoutConfig` and re-render on the next interval.

## Implementation Strategy

### Phase 1: Layout Config Refactor

Introduce `wily/ui/watch_layout.py` (already drafted) that centralizes width calculations, panel visibility, and responsive breakpoints. This separates layout policy from rendering.

### Phase 2: Grouped Task Rendering

Modify `wily/ui/watch_render.py`:
- Split `build_rows` into `build_grouped_rows` that returns a dict of `{status: [WatchRow]}`.
- Render each group with a header rule line.
- Add `meta` column generation (depends, claimed time, done time).

### Phase 3: Activity Panel Renderer

Add `wily/ui/watch_activity.py`:
- Consumes `tasks`, `actors`, `cp_summaries`.
- Returns a list of string lines for the right panel.
- Only invoked when `WatchLayoutConfig.show_activity_panel` is true.

### Phase 4: Checkpoint Timeline

Extend `CpSummary` in `wily/progress.py` to include checkpoint names in order (derived from `progress.jsonl` event history). Timeline rendering consumes this ordered list.

### Phase 5: Keyboard Toggles

Add `--interactive` flag to `wily/cli/watch.py`. Use `tty.setcbreak` + `select` on stdin to read single keystrokes without blocking the sleep interval.

### ASCII Mode Parity

Every rich feature must have an ASCII equivalent:
- Group headers: `--- IN PROGRESS ---`
- Timeline: `plan > design > [implement] > test > deploy`
- Activity panel: plain text table with `|` separators.
- Colors: no ANSI; use `* ~ > x` glyphs only.

## Files to Modify

| File | Change |
|------|--------|
| `wily/ui/watch_layout.py` | **New**. Responsive layout configuration. |
| `wily/ui/watch_render.py` | Refactor to use `WatchLayoutConfig`, add grouped rendering, meta columns, timeline. |
| `wily/ui/watch_activity.py` | **New**. Actor activity panel renderer. |
| `wily/progress.py` | Add checkpoint ordered list to `CpSummary`. |
| `wily/cli/watch.py` | Add `--compact`, `--show-timeline`, `--hide-log`, `--interactive` flags. |
| `tests/v3/test_v3_core.py` | Add tests for grouped rows, layout config breakpoints, activity panel output. |
| `skills/wily-watch/SKILL.md` | Document new flags and keyboard shortcuts. |

## Acceptance Criteria

1. `wily watch --once --ui ascii` still produces clean, scannable output (backward compat).
2. `wily watch --once --ui rich` shows status groups with header rules.
3. In a 120+ col terminal, `wily watch` shows tasks + activity side-by-side.
4. In a 72 col terminal, `wily watch` shows compact single-column with no activity panel.
5. Checkpoint timeline renders correctly when checkpoints exist.
6. All new code has unit tests in `tests/v3/test_v3_core.py`.
7. No v2 concepts (stage, phase, board) leak into the UI.
