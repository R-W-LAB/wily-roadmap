# Wily Board Live Overlay Design

## Purpose

Wily Board should show what collaborators are doing before their `.wily/` changes are pushed. This must improve coordination without weakening the current source-of-truth model.

The durable roadmap state remains each repository's committed `.wily/` files. Live Board state is an overlay: useful for presence, claims, local completion, and blockers, but not an authoritative phase transition until GitHub sync confirms it from the repository.

## Current Baseline

- Wily Board is a separate FastAPI, SQLite, and htmx application in `R-W-LAB/wily-board`.
- Board sync currently reads `.wily/roadmap.yaml` and `.wily/**/stage.yaml` from GitHub.
- Repository workflows notify Board on pushes touching `.wily/**`.
- Board write actions create GitHub pull requests instead of directly pushing to default branches.
- Wily CLI commands such as `start`, `complete`, and `block` already update local `.wily` state through deterministic script paths.

## Design Summary

Add a live overlay layer to Board.

Durable state answers: "What does the repository say?"

Live state answers: "What is someone doing locally right now?"

Board renders both together. A phase may have durable status `pending` while the live overlay says `airmang is working locally`. A phase may have durable status `in_progress` while another collaborator sees a stale live heartbeat and knows the local session may have gone quiet.

## Status Model

Live statuses are separate from stored roadmap statuses.

- `claimed`: a user started or retried a phase locally.
- `active`: the CLI has recently sent a heartbeat for the session.
- `blocked_local`: the local session recorded a blocker before push.
- `completed_local`: the user completed the phase locally, but the committed roadmap has not caught up.
- `stale`: Board has not received a heartbeat within the stale window.
- `cleared`: the durable GitHub state now reflects the live transition, so the overlay can be hidden or archived.

Stored roadmap statuses stay unchanged:

- `pending`
- `ready`
- `in_progress`
- `needs_review`
- `done`
- `blocked`
- `superseded`

## Event Flow

### Start

When `$wily-start <phase-id>` succeeds:

1. Wily CLI creates the local session and marks the local phase or stage phase `in_progress`.
2. If Board live sync is configured, Wily CLI sends a signed live event:
   - repo full name
   - local repo root fingerprint or path label
   - phase id
   - stage id when known
   - actor
   - session id or relative session path
   - live status `claimed`
   - timestamp
3. Board upserts the live session and shows it on the affected phase row.

### Heartbeat

During active work, the CLI or a lightweight helper may send heartbeat events:

- event type: `heartbeat`
- live status: `active`
- optional note: `editing`, `running tests`, `waiting for review`, or a short user-provided note
- last seen timestamp

The first implementation can skip continuous background heartbeats and rely on command-triggered events. Continuous heartbeats can be added as an opt-in follow-up.

### Block

When `$wily-block <phase-id> "<reason>"` succeeds:

1. Wily CLI records the local blocker in `.wily`.
2. It sends live status `blocked_local` with the blocker reason.
3. Board displays the blocker as local until GitHub sync confirms a durable `blocked` state.

### Complete

When `$wily-complete <phase-id>` succeeds:

1. Wily CLI marks the local roadmap state `done`.
2. It sends live status `completed_local`.
3. Board displays `completed locally - awaiting push`.
4. After a push-triggered GitHub sync sees durable `done`, Board clears the overlay.

Board must not display push-before-complete as official `done`. The visual language should make local completion feel useful but provisional.

### GitHub Sync

After the existing GitHub webhook sync completes:

1. Board compares durable phase status with live overlay records.
2. If durable status has caught up, Board marks matching live records `cleared` or hides them.
3. If durable status contradicts live status, Board keeps the overlay but labels it as stale or conflicting.

Examples:

- durable `done` plus live `completed_local`: clear overlay.
- durable `blocked` plus live `blocked_local`: clear overlay or show as confirmed.
- durable `pending` plus live `completed_local`: show `completed locally - awaiting push`.

## Board API

Add a signed endpoint:

```text
POST /api/live/events
```

Headers:

```text
X-Wily-Signature: sha256=<hmac>
Content-Type: application/json
```

Payload:

```json
{
  "repo": "R-W-LAB/wily-roadmap",
  "phase_id": "16-1",
  "stage_id": "s16",
  "actor": "airmang",
  "event": "start",
  "live_status": "claimed",
  "session_path": "sessions/2026-05-16-120000-phase-16-1-attempt-1",
  "note": "",
  "client_time": "2026-05-16T12:00:00Z"
}
```

The endpoint uses the existing `WILY_BOARD_SECRET` HMAC model for the first implementation. Per-user or per-repo live tokens are out of scope for this design.

## Board Data Model

Add a `live_sessions` table:

```sql
CREATE TABLE IF NOT EXISTS live_sessions (
  id INTEGER PRIMARY KEY,
  repo_id INTEGER NOT NULL REFERENCES repos(id) ON DELETE CASCADE,
  phase_id TEXT NOT NULL,
  stage_id TEXT,
  actor TEXT NOT NULL,
  session_path TEXT,
  live_status TEXT NOT NULL,
  note TEXT,
  first_seen_at TEXT NOT NULL,
  last_seen_at TEXT NOT NULL,
  cleared_at TEXT,
  payload_json TEXT NOT NULL,
  UNIQUE(repo_id, phase_id, actor, session_path)
);
```

The uniqueness key allows one actor to retry a phase with a new session without overwriting prior attempt history.

Add `live_events` only if audit detail is needed. The first version can append event payloads to the existing `events` table and keep `live_sessions` as the current overlay cache.

## Wily CLI Configuration

Live sync must be opt-in.

Recommended config sources, in priority order:

1. Environment variables:
   - `WILY_BOARD_URL`
   - `WILY_BOARD_SECRET`
   - `WILY_BOARD_REPO`
   - `WILY_BOARD_ACTOR`
2. Optional local config file outside git:
   - `$HOME/.config/wily/board.env`
3. Repository-local untracked config:
   - `.wily/local/board.env`

Do not store secrets in committed `.wily` files.

If live sync is not configured, Wily CLI commands continue to work exactly as they do now and print a concise note only when useful.

## CLI Integration Points

Add a small live event helper in the Wily plugin scripts.

Call it after successful local state writes in:

- `command_start`
- `command_complete`
- `command_block`

Do not emit live events from `command_replan` or `command_decompose_stage` in the first implementation. Those commands alter roadmap structure rather than a single active work session.

The helper must be best-effort:

- never fail the Wily command because Board is down
- use short network timeouts
- avoid sending secrets to stdout
- report only concise diagnostics in verbose/debug mode

The initial implementation should send events only at command boundaries. Continuous activity signals such as `wily live-heartbeat` or `wily watch --board-heartbeat` are separate follow-up work.

## UI Behavior

Board phase rows should render durable status and live overlay separately.

Examples:

- Durable `pending`, live `claimed`:
  - status text: `pending`
  - live chip: `airmang working locally`

- Durable `in_progress`, live `active`:
  - status text: `in progress`
  - live chip: `active now`

- Durable `pending`, live `completed_local`:
  - status text: `pending`
  - live chip: `completed locally - awaiting push`

- Durable `blocked`, live cleared:
  - status text: `blocked`
  - no live chip

Active dashboard sections should include live overlays:

- `Active right now` includes live `claimed`, `active`, and recent `blocked_local`.
- `Up next` excludes phases claimed by another active user unless the durable state says they are still available and the live record is stale.
- Repo detail pages show live chips on phase rows.

The chip should be visually lighter than the durable status dot. This keeps the official roadmap status legible.

## Staleness

Use two thresholds:

- fresh: last seen within 2 minutes
- stale: last seen older than 5 minutes

Fresh overlays appear in `Active right now`.

Stale overlays remain visible on repo detail rows as `stale local session`, but should not block a phase from appearing in `Up next`.

The exact thresholds should be settings:

- `LIVE_FRESH_SECONDS`, default `120`
- `LIVE_STALE_SECONDS`, default `300`

## Conflict Handling

Board should tolerate contradictions because live state is provisional.

Conflict examples:

- two actors claim the same phase
- a live session says `completed_local`, but durable state remains `pending` for a long time
- durable state moves to `done`, but a live heartbeat still arrives from an old session

Rules:

- Show multiple active actors when they exist.
- Prefer durable state for the main status dot and progress counts.
- Do not hide conflicting live state unless it is cleared or stale.
- When durable state reaches `done`, ignore new heartbeats for older session paths unless a retry session appears.

## Security

Use signed events. Unsigned or invalid signatures return `401`.

The first version reuses `WILY_BOARD_SECRET`. Per-user or per-repo live tokens are separate follow-up work to reduce blast radius.

Do not expose local filesystem paths beyond the `.wily` relative session path. If a local absolute path is useful for debugging, hash or omit it.

Do not allow live events to mutate durable roadmap tables directly. They only update live overlay tables.

## Testing

Wily plugin tests:

- live event payload generation for start, complete, and block
- no network call when config is absent
- Board failures do not fail lifecycle commands
- stage-child phase ids include stage metadata when available

Board tests:

- signed `/api/live/events` accepts valid payloads and rejects invalid signatures
- live event upserts `live_sessions`
- GitHub sync clears matching `completed_local` overlays
- active and stale overlays affect `Active right now` and `Up next` queries correctly
- templates render live chips without changing durable status display

Manual verification:

1. Run Board locally.
2. Configure Wily CLI with local Board URL and secret.
3. Run `$wily-start <phase-id>`.
4. Confirm Board shows the phase as locally claimed before commit or push.
5. Run `$wily-complete <phase-id>`.
6. Confirm Board shows `completed locally - awaiting push`.
7. Push `.wily` changes and confirm GitHub sync clears the overlay.

## Rollout

1. Add Board storage, API, and query support.
2. Add UI live chips and dashboard query behavior.
3. Add Wily CLI best-effort event emission.
4. Configure one local repository for live sync.
5. Verify start, block, complete, stale, and push-clear flows.
6. Document production configuration in Wily Board operations.

## Non-Goals

- Do not make Board the source of truth for roadmap progress.
- Do not auto-push `.wily` changes from Wily CLI.
- Do not add MCP servers, app integrations, or plugin hooks for this feature.
- Do not make local live completion count as official `done`.
- Do not require live sync for normal Wily CLI usage.
