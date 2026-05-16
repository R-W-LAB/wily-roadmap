# Wily Board Live Draft Topology Design

Date: 2026-05-17

## Problem

Wily Roadmap can decompose a Stage locally before the resulting `.wily` files are committed and pushed. `wily status` immediately shows the decomposed child phases, but Wily Board does not.

The current realtime implementation covers presence-style local activity:

- an actor claimed a Stage or Phase
- an actor is actively working
- an actor completed or blocked work locally and is awaiting push

It does not cover topology-style local changes:

- a Stage was decomposed locally
- new child Phase rows exist locally
- Board should render those child Phases before durable GitHub sync catches up

This creates a mismatch with the expected operating model: Wily Roadmap should show local Stage/Phase planning changes in Wily Board immediately, then reconcile them with durable `.wily` state after commit and push.

## Goals

- Show locally decomposed Stage child Phases on Wily Board before commit and push.
- Keep committed `.wily` Git state as the durable source of truth.
- Mark local topology as provisional with clear `local draft` and `awaiting push` language.
- Reconcile provisional topology automatically when GitHub sync imports the matching durable `stage.yaml`.
- Preserve the existing live heartbeat and work-signal model for presence.
- Keep remote actions approval-first and local-first.

## Non-Goals

- Do not make Board write directly into user repositories.
- Do not replace GitHub sync as the durable roadmap ingestion path.
- Do not add MCP servers, app integrations, or workspace permission systems.
- Do not make Board poll developer machines or read their local files directly.
- Do not build a full collaborative editing model for arbitrary `.wily` file diffs.

## Recommended Architecture

Add a separate live draft topology path alongside the existing live presence path.

Presence events remain in `live_items` and `live_sessions`. They answer: "who is working on what right now?"

Topology draft events go into a new `live_drafts` table. They answer: "what local roadmap structure exists before it is pushed?"

This separation keeps the existing heartbeat semantics small and stable while letting Board render provisional child Phases from structured draft payloads.

## Event Contract

`wily decompose-stage` sends a signed `POST /api/live/events` event after a decomposition is applied locally.

Required payload fields:

```json
{
  "repo": "R-W-LAB/wily-roadmap",
  "item_type": "stage",
  "item_id": "s21",
  "stage_id": "s21",
  "actor": "airmang",
  "agent": "codex",
  "event": "stage_decomposed_local",
  "live_status": "active",
  "draft_kind": "stage_decomposition",
  "session_id": "local-session-id",
  "phases": [
    {
      "id": "21-1",
      "title": "Contract reconciliation and implementation plan",
      "status": "pending",
      "depends_on": [],
      "owner": "codex",
      "task": "reconcile the redesign spec with the current Board codebase",
      "path": "stages/s21-wily-board-ui-redesign/phases/21-1-contract-reconciliation-plan"
    }
  ]
}
```

Validation rules:

- `draft_kind` must be `stage_decomposition`.
- `item_type` must be `stage`.
- `item_id` and `stage_id` must match.
- `phases` must be a non-empty list.
- Each draft phase must include `id` and `title`.
- Optional phase fields are normalized to strings or lists of strings.
- Invalid draft payloads return HTTP 400 and do not mutate Board state.

## Wily CLI Behavior

`decompose-stage` keeps its current local file behavior. After writing `stage.yaml`, child Phase files, and `roadmap.yaml`, it attempts to emit the live draft event.

If Board live config is missing, the command still succeeds locally and prints:

```text
Board live draft not sent: missing WILY_BOARD_URL, WILY_BOARD_SECRET, WILY_BOARD_REPO, or WILY_BOARD_ACTOR.
```

If Board returns an HTTP error, the command still succeeds locally and prints the response status in a concise warning.

If Board accepts the event, the command prints:

```text
Board live draft sent for s21: 7 phases
```

The command reads Board config from the existing sources:

- environment variables
- `~/.wily/board.json`
- `.wily/local/board.json`

No secrets are written into tracked files.

## Board Storage

Add `live_drafts`:

```sql
CREATE TABLE IF NOT EXISTS live_drafts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  repo_id INTEGER NOT NULL REFERENCES repos(id) ON DELETE CASCADE,
  draft_kind TEXT NOT NULL,
  item_type TEXT NOT NULL,
  item_id TEXT NOT NULL,
  stage_id TEXT NOT NULL,
  actor TEXT NOT NULL,
  agent TEXT NOT NULL,
  session_id TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  last_seen_at TEXT NOT NULL,
  cleared_at TEXT,
  UNIQUE(repo_id, draft_kind, stage_id, actor, session_id)
);
```

`payload_json` stores the normalized draft payload. Board can render provisional Phases without trying to project them into durable `stages` and `phases` tables.

## Board Rendering

Repository detail merges durable and provisional data at render time:

- Durable `stages` and `phases` remain the primary dataset.
- If a Stage has a live `stage_decomposition` draft, Board renders the draft child Phases under that Stage.
- Draft rows display `local draft`, `awaiting push`, and `actor/agent`.
- Draft rows must not expose durable mutation controls.
- If durable child Phases for the same Stage already exist, durable rows win and matching drafts are omitted.

Dashboard surfaces add a concise follow-up item:

```text
S-21 decomposed locally - 7 draft phases awaiting push
```

This item links to the repository detail Stage anchor.

## Reconciliation

During durable GitHub sync, after `.wily/roadmap.yaml` and `*/stage.yaml` files are imported:

- If a synced Stage contains durable child Phases, clear matching `live_drafts` for that `repo_id` and `stage_id`.
- Clearing means setting `cleared_at`, not deleting rows.
- Cleared drafts are excluded from dashboard and repo detail rendering.
- Existing `live_items` clearing behavior stays unchanged.

This makes the Board transition from provisional topology to durable topology without duplicate rows.

## Error Handling

- Missing CLI config is a visible warning, not a command failure.
- HTTP/network failures are visible warnings, not command failures.
- Board rejects malformed draft payloads with 400.
- Board rejects unknown repositories with 404.
- Board rejects invalid HMAC signatures with 401.
- Rendering ignores malformed stored draft JSON defensively and leaves durable data visible.

## Testing

Wily Roadmap tests:

- `decompose-stage --from-json` emits `stage_decomposed_local` when Board config exists.
- `decompose-stage --from-json` succeeds and warns when Board config is missing.
- emitted payload includes normalized child Phase data and `draft_kind=stage_decomposition`.

Wily Board tests:

- live draft event is accepted and stored.
- malformed draft event is rejected.
- repo detail renders provisional child Phases for a Stage with no durable child Phases.
- repo detail prefers durable child Phases when both durable and draft topology exist.
- dashboard renders a follow-up item for draft topology awaiting push.
- durable sync clears matching draft topology.

## Success Criteria

- Decomposing S-21 locally makes `21-1` through `21-7` visible on Board before commit and push.
- Board clearly marks those rows as provisional local draft state.
- Pushing the `.wily` files and running GitHub sync replaces provisional rows with durable rows.
- Missing local Board config is immediately visible in CLI output.
- The feature does not change durable roadmap progress or push to repositories.

## Self-Review

- No placeholder requirements remain.
- The design keeps presence and topology concerns separate.
- The design preserves committed `.wily` state as the durable source of truth.
- The draft payload contains enough Phase data to render Board rows before GitHub sync.
- The reconciliation rule is deterministic and scoped by repository and Stage.
