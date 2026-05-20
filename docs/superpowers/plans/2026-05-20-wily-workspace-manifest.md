# Wily Workspace Manifest Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add parent-workspace multi-repo visibility to the Wily Roadmap plugin without creating a parent `.wily/` source of truth.

**Architecture:** Introduce a manifest-only workspace layer via `wily-workspace.yaml` or `.wily-workspace.yaml`. The new `wily workspace` command reads configured child repo paths, loads each child repo's own `.wily/tasks.yaml`, and renders aggregated status/next output while leaving claim/go/done in each child repo.

**Tech Stack:** Python stdlib + PyYAML, existing Wily v3 CLI dispatcher, existing task loaders and scheduling helpers, unittest-based v3 tests.

---

## File Structure

- Create `plugins/wily-roadmap/scripts/wily/workspace.py`
  - Manifest discovery, parsing, repo validation, aggregate summaries, and JSON-serializable payloads.
- Create `plugins/wily-roadmap/scripts/wily/cli/workspace.py`
  - CLI subcommands: `status`, `next`, `watch`, `init`, and `show-config`.
- Modify `plugins/wily-roadmap/scripts/wily/cli/_common.py`
  - Add `workspace` to `COMMANDS`; remove or update any wording that implies no dashboard/workspace integration where necessary.
- Modify `plugins/wily-roadmap/scripts/wily/cli/__main__.py` only if subcommand dispatch needs special handling.
- Create `plugins/wily-roadmap/commands/workspace.md`
  - Command docs for parent workspace operation.
- Create `plugins/wily-roadmap/skills/wily-workspace/SKILL.md`
  - Skill guidance for `$wily-workspace`.
- Modify `plugins/wily-roadmap/tests/v3/test_v3_core.py`
  - Unit tests for manifest parsing, discovery, aggregation, and subcommands.
- Modify `plugins/wily-roadmap/tests/v3/test_v3_surface.py`
  - Surface tests for command and skill registration/docs/help.
- Optionally modify `plugins/wily-roadmap/README.md`
  - Short workspace manifest example.

## Task 1: Manifest Model And Discovery

**Files:**
- Create: `plugins/wily-roadmap/scripts/wily/workspace.py`
- Test: `plugins/wily-roadmap/tests/v3/test_v3_core.py`

- [ ] **Step 1: Write failing tests for manifest discovery**

Add tests that create a temporary parent directory with `wily-workspace.yaml` and two child repos, then assert:

```python
from wily.workspace import discover_workspace_manifest, load_workspace

manifest = discover_workspace_manifest(parent / "nested")
self.assertEqual(manifest, parent / "wily-workspace.yaml")

workspace = load_workspace(manifest)
self.assertEqual(workspace.title, "Wily Plugin Workspace")
self.assertEqual([repo.id for repo in workspace.repos], ["wily-roadmap", "wily-board"])
```

Expected behavior:
- Searches upward from cwd.
- Accepts `wily-workspace.yaml` first, then `.wily-workspace.yaml`.
- Does not create or require parent `.wily/`.

- [ ] **Step 2: Run test and verify RED**

Run:

```bash
python3 -m unittest plugins.wily-roadmap.tests.v3.test_v3_core.CoreModelTest.test_workspace_manifest_discovery
```

Expected: import failure for `wily.workspace` or missing function.

- [ ] **Step 3: Implement minimal manifest discovery and parser**

Implement:

```python
@dataclass(frozen=True)
class WorkspaceRepo:
    id: str
    path: Path
    group: str | None = None
    role: str | None = None

@dataclass(frozen=True)
class WorkspaceConfig:
    title: str
    root: Path
    repos: list[WorkspaceRepo]
```

Parser rules:
- `schema` must be `wily-workspace-v1`.
- `repos[].id` and `repos[].path` are required.
- Repo paths are resolved relative to the manifest directory.
- Duplicate repo ids are rejected.

- [ ] **Step 4: Run tests and verify GREEN**

Run the targeted manifest tests, then:

```bash
python3 -m unittest plugins/wily-roadmap/tests/v3/test_v3_core.py -k workspace
```

Expected: workspace tests pass.

## Task 2: Aggregate Repo State

**Files:**
- Modify: `plugins/wily-roadmap/scripts/wily/workspace.py`
- Test: `plugins/wily-roadmap/tests/v3/test_v3_core.py`

- [ ] **Step 1: Write failing tests for aggregate summaries**

Create two child repos with `.wily/tasks.yaml`:
- `wily-roadmap`: one ready task.
- `wily-board`: one in-progress task and one blocked task.

Assert aggregate payload includes:
- project title per repo
- done/total counts
- in-progress tasks
- next ready task from `parallel_candidates`
- blocked tasks
- missing/invalid repos marked as errors, not crashes

- [ ] **Step 2: Run test and verify RED**

Expected: aggregate helper missing.

- [ ] **Step 3: Implement aggregation**

Implement helper names such as:

```python
def workspace_snapshot(config: WorkspaceConfig) -> dict[str, object]:
    ...
```

Use existing:
- `WilyPaths`
- `load_tasks`
- `load_actors`
- `repo_mode`
- `parallel_candidates`
- `waiting_candidates`
- `cp_summary`

Do not duplicate task state into parent files.

- [ ] **Step 4: Run targeted tests**

Expected: aggregate summary handles healthy and missing repos.

## Task 3: CLI Command `wily workspace`

**Files:**
- Create: `plugins/wily-roadmap/scripts/wily/cli/workspace.py`
- Modify: `plugins/wily-roadmap/scripts/wily/cli/_common.py`
- Test: `plugins/wily-roadmap/tests/v3/test_v3_core.py`

- [ ] **Step 1: Write failing CLI tests**

Test:
- `wily workspace status --json`
- `wily workspace next --json`
- `wily workspace init --repo wily-roadmap=./wily-roadmap --repo wily-board=./wily-board`
- `wily workspace show-config`
- parent cwd with no manifest fails with a Korean/English-friendly actionable error.

- [ ] **Step 2: Run test and verify RED**

Expected: unknown command `workspace`.

- [ ] **Step 3: Register command**

Add `"workspace"` to `_common.COMMANDS`.

- [ ] **Step 4: Implement command module**

CLI contract:

```text
wily workspace status [--json] [--repo <id>] [--group <group>]
wily workspace next [--json] [--repo <id>] [--group <group>]
wily workspace watch [--once] [--interval <seconds>] [--json]
wily workspace init --repo <id=path> [--repo <id=path> ...] [--title <text>]
wily workspace show-config [--json]
```

Exit codes:
- `0`: all repos done or command successful.
- `1`: any repo has ready/in-progress work.
- `2`: any repo has blocked work.
- usage/failure codes follow `_common`.

- [ ] **Step 5: Run targeted CLI tests**

Expected: JSON and text outputs are stable enough for agents and humans.

## Task 4: Watch And Text Rendering

**Files:**
- Modify: `plugins/wily-roadmap/scripts/wily/cli/workspace.py`
- Test: `plugins/wily-roadmap/tests/v3/test_v3_core.py`

- [ ] **Step 1: Write failing watch tests**

Test:
- `workspace watch --once` delegates to one-shot status.
- `workspace watch --interval 0` is rejected.
- normal watch redraws when any child repo `.wily/.touch` mtime changes.

- [ ] **Step 2: Implement watch loop**

Keep it simple:
- No tmux pane support for v1.
- Use polling interval.
- Track max child `.wily/.touch` mtime.
- `--once` exits after one render.

- [ ] **Step 3: Run targeted tests**

Expected: watch helper behavior matches existing `wily watch` conventions.

## Task 5: Docs, Skill, And Surface Registration

**Files:**
- Create: `plugins/wily-roadmap/commands/workspace.md`
- Create: `plugins/wily-roadmap/skills/wily-workspace/SKILL.md`
- Modify: `plugins/wily-roadmap/tests/v3/test_v3_surface.py`
- Modify: `plugins/wily-roadmap/README.md`

- [ ] **Step 1: Write failing surface tests**

Update `COMMANDS` and `SKILLS` sets in `test_v3_surface.py` to include workspace.

Assert:
- command docs mention manifest-only behavior
- skill docs say parent `.wily/` is not created
- README includes a `wily-workspace.yaml` example
- help output includes `workspace`

- [ ] **Step 2: Add docs and skill**

Docs must state:
- Parent manifest is not source of truth.
- Child `.wily/` ledgers remain authoritative.
- `workspace` commands do not claim/go/done across repos.
- Use per-repo commands for state transitions.

- [ ] **Step 3: Run surface tests**

Expected: command/skill registry is consistent.

## Task 6: Final Verification

**Files:**
- Verification only.

- [ ] **Step 1: Run focused tests**

```bash
python3 -m unittest plugins.wily-roadmap.tests.v3.test_v3_core -k workspace
python3 -m unittest plugins.wily-roadmap.tests.v3.test_v3_surface
```

- [ ] **Step 2: Run full plugin tests**

```bash
python3 -m unittest plugins.wily-roadmap.tests.v3.test_v3_core plugins.wily-roadmap.tests.v3.test_v3_surface
```

- [ ] **Step 3: Manual smoke from parent workspace**

From `/Users/wilycastle/Code/projects/wily-plugin`:

```bash
python3 wily-roadmap/plugins/wily-roadmap/scripts/wily.py workspace status --json
python3 wily-roadmap/plugins/wily-roadmap/scripts/wily.py workspace next
python3 wily-roadmap/plugins/wily-roadmap/scripts/wily.py workspace watch --once
```

Expected:
- Sees `wily-roadmap` and `wily-board` from `wily-workspace.yaml`.
- Shows per-repo next tasks.
- Does not create parent `.wily/`.
