# Wily Board Local Activity Heartbeat Plan

## Goal

Wily Board should show what Wily agents are doing right now, even before `.wily/` changes are committed and pushed.

Target experience:

1. A user or agent creates or starts a local Stage such as `s21`.
2. Board immediately shows that local work exists.
3. While Codex or Claude is working, Board receives heartbeat updates and shows the agent as active.
4. If the heartbeat stops, Board marks the work stale instead of pretending it is still active.
5. When `.wily/` is committed and pushed, GitHub sync confirms the durable state and Board connects or clears the provisional local overlay.

This is not meant to replace Git as the durable source of truth. It is a live operating layer for coordination.

## Current Problem

The current Board model has two layers:

- Durable roadmap state from GitHub: committed `.wily/roadmap.yaml` and `.wily/**/stage.yaml`.
- Live overlay state: local start, block, complete, and heartbeat events.

The live overlay currently assumes the durable Stage or Phase already exists in Board DB. Board queries join `live_sessions` to durable `stages` and `phases`, so a brand-new local Stage that has not been pushed yet cannot reliably appear on the Board.

This means:

- `wily status` can show a local `s21`.
- Board cannot show `s21` as durable until `.wily/roadmap.yaml` is pushed and synced.
- A heartbeat for `s21` may be stored, but it has no durable row to attach to, so it is not a first-class visible work item.

## Design Principle

Keep two truths separate:

- Durable truth: GitHub-synced `.wily` state.
- Live truth: signed local activity events from Wily CLI or agent-side heartbeat.

Board should render both. If a live item has no durable row yet, show it as `local only` or `awaiting push`.

## User Model

Heartbeat should feel automatic while a Wily work session is active, and Board should reflect not just "the process is alive" but "the agent just did something."

Recommended behavior:

```text
wily start s21 --agent codex
  -> generates session_id
  -> marks local roadmap state in_progress
  -> sends created_local (if new) and claimed
  -> writes .wily/local/live/active/<session-id>.json   (hooks discover via this file, not env var)
  -> forks a detached sidecar with --parent-shell-pid $$
  -> returns immediately; terminal stays free
  -> Board chip: codex · active

Codex or Claude works in the same or another pane
  -> sidecar sends heartbeat every 30s  (chip stays "active")
  -> agent's PostToolUse hook reads the active/ registry, finds the matching session,
     and sends `worked` (token-zero — model never sees this)
  -> Board chip flips to "codex · working" within ~1s,
     stays there for LIVE_WORK_SECONDS after the last work

User goes to lunch
  -> heartbeats keep arriving but no `worked` events
  -> Board chip drops back to "active" after LIVE_WORK_SECONDS
  -> after LIVE_FRESH_SECONDS with only heartbeats, chip becomes "idle"

User closes the terminal
  -> parent-shell PID disappears, sidecar notices within ~10s
  -> sidecar emits `released` and exits, .alive file removed
  -> Board chip transitions to "stale" after LIVE_STALE_SECONDS

wily replan renames s21 -> s22
  -> Wily CLI emits renamed(session_id=SID-W, old=s21, new=s22)
  -> Board updates current_item_id for that live row
  -> chip continues seamlessly under the new slug

wily complete s22
  -> sends completed_local
  -> removes .alive; sidecar exits on next tick
  -> Board chip: completed locally — awaiting push

git push .wily changes
  -> GitHub webhook syncs durable state
  -> Board attaches the local overlay using session_id ↔ current_item_id mapping
     it has been maintaining from the event stream (no session_id in YAML)
```

The terminal stays free throughout. The sidecar is a small, well-behaved background process tied to the launching shell's lifetime, not a global daemon.

## Configuration

Live activity should be opt-in once per machine or repo.

Config sources, in priority order:

1. Process environment:
   - `WILY_BOARD_URL`
   - `WILY_BOARD_SECRET`
   - `WILY_BOARD_REPO`
   - `WILY_BOARD_ACTOR`
   - `WILY_BOARD_AGENT`
   - `WILY_BOARD_HEARTBEAT`
2. User config:
   - `$HOME/.config/wily/board.env`
3. Repo-local untracked config:
   - `.wily/local/board.env`

Example:

```sh
WILY_BOARD_URL=https://rnwlab.duckdns.org
WILY_BOARD_SECRET=<same HMAC secret used by Board>
WILY_BOARD_REPO=R-W-LAB/wily-roadmap
WILY_BOARD_ACTOR=airmang
WILY_BOARD_AGENT=codex
WILY_BOARD_HEARTBEAT=1
```

`WILY_BOARD_AGENT` should be explicit. Do not rely on fragile process detection. Codex, Claude, or a human terminal can set the value.

## Live Event Contract

Extend the live payload so it can represent local-only Stage, Phase, or repo-level activity, and so Board can distinguish "process alive" from "agent doing work right now."

Required fields:

```json
{
  "repo": "R-W-LAB/wily-roadmap",
  "item_type": "stage",
  "item_id": "s21",
  "item_title": "Wily Board UI redesign",
  "actor": "airmang",
  "agent": "codex",
  "event": "heartbeat",
  "live_status": "active",
  "local_only": true,
  "session_id": "01HW...",
  "session_path": ".wily/sessions/...",
  "client_time": "2026-05-16T14:30:00Z"
}
```

`session_id` is a client-generated ULID/UUID that survives slug renames, replans, and reconnects. It is the canonical key for joining live events to a single work session and, after push, to a durable Stage/Phase (see "Attach Resolution").

Optional fields for work-signal events (see "Agent Work Signals"):

```json
{
  "event": "worked",
  "live_status": "working",
  "work": {
    "kind": "tool_call",
    "tool": "Edit",
    "tokens_in": 1284,
    "tokens_out": 312,
    "summary": "edited app/db/repo.py"
  }
}
```

Compatibility fields:

- Keep accepting `phase_id` and `stage_id` from the current implementation.
- When `item_type` is missing, infer from old fields where possible.
- Events missing `session_id` are accepted but treated as anonymous — they can never attach to a durable row after push and are aged out aggressively.

Events:

- `created_local`: local Stage or Phase exists before push.
- `claimed`: an actor started a Wily session.
- `heartbeat`: process-alive ping.
- `worked`: agent just performed a unit of work (tool call, edit, step completion).
- `blocked_local`: local blocker recorded before push.
- `completed_local`: local completion recorded before push.
- `released`: session ended cleanly without complete/block (e.g., explicit stop).

Derived live statuses (Board sets these from events + server clock):

- `working`: a `worked` event arrived inside the **working window** (default 90s).
- `active`: a `heartbeat` arrived inside the **fresh window** (default 60s) but no recent `worked`.
- `idle`: a `heartbeat` arrived inside the **stale window** (default 5m) but neither working nor active.
- `stale`: no signal for longer than the stale window.
- `completed_local` / `blocked_local`: terminal-local states until durable sync.
- `cleared`: derived by Board after durable sync confirms or supersedes the overlay.

All windows are server-side and live in Board config so they can be tuned without a client release.

## Board Data Model

Prefer adding a general live activity table rather than forcing all live state into phase-only joins. Make `session_id` the primary join key so attach survives renames and concurrent sessions don't collide.

Proposed table:

```sql
CREATE TABLE live_items (
  id INTEGER PRIMARY KEY,
  repo_id INTEGER NOT NULL REFERENCES repos(id) ON DELETE CASCADE,
  session_id TEXT NOT NULL,
  item_type TEXT NOT NULL,
  item_id TEXT NOT NULL,
  current_item_id TEXT NOT NULL,
  item_title TEXT,
  stage_id TEXT,
  phase_id TEXT,
  actor TEXT NOT NULL,
  agent TEXT NOT NULL,
  session_path TEXT NOT NULL DEFAULT '',
  live_status TEXT NOT NULL,
  local_only INTEGER NOT NULL DEFAULT 0,
  note TEXT,
  first_seen_at TEXT NOT NULL,    -- server clock
  last_seen_at TEXT NOT NULL,     -- server clock, updated on every event
  last_worked_at TEXT,            -- server clock of most recent `worked` event
  last_heartbeat_at TEXT,         -- server clock of most recent `heartbeat`
  last_client_time TEXT,          -- client-asserted time, kept for forensics only
  cleared_at TEXT,
  attached_durable_id INTEGER,    -- FK to durable stage/phase row after sync
  payload_json TEXT NOT NULL,
  UNIQUE(repo_id, session_id, item_type)
);

CREATE INDEX live_items_recent
  ON live_items(repo_id, last_seen_at DESC)
  WHERE cleared_at IS NULL;
```

Notes:

- The unique key is `(repo_id, session_id, item_type)` rather than the previous tuple involving `session_path`. `session_path` was unreliable (empty strings collapsed rows, timestamped paths exploded them). `session_id` is the contract.
- Multiple agents working on the same `item_id` produce **separate rows** (different `session_id`), so the Board can render one chip per `(actor, agent)`. There is no last-write-wins.
- `last_seen_at`, `last_worked_at`, `last_heartbeat_at` are **server clock only**. The client's `client_time` is recorded for diagnostics but never drives freshness.

`live_sessions` can remain for backwards compatibility during migration. The "Implementation Phases" section below explicitly absorbs the `heartbeat-freshness` plan's Tasks 1–2 into Phase 1 so we don't ship two parallel implementations.

### Attach Resolution

Durable `.wily/` never carries `session_id`. The principle "sessions are local" stays intact — committed YAML contains only roadmap state. Board derives the `session_id ↔ current item_id` mapping from the **event stream**, which is already a first-class signal.

Wily CLI emits the following events during a session's lifetime:

- `created_local(session_id, item_id=s21)` — when a local Stage is authored.
- `renamed(session_id, old_item_id=s21, new_item_id=s22)` — when `wily replan` or any roadmap rename changes the slug while the session is still local. The session id is the same; only `item_id` changes.
- `completed_local(session_id, item_id=s22)` — terminal local event before push.

Board maintains a per-row `current_item_id` (initially the most recent rename target). When the GitHub webhook fires and the durable `.wily/` parser creates a Stage row for `s22`:

1. Look up unattached `live_items` rows where `current_item_id = 's22'` (and item_type matches).
2. Set `attached_durable_id` on each match. Multiple actors/agents on the same renamed stage all attach.
3. If no match exists, fall back to `(item_type, item_id)` against the most-recent `created_local` for that slug (covers cases where the session never sent a `renamed` event because the slug never changed).
4. Leave the row visible after attach; the next terminal event clears it. Attached overlays explain "this Stage was started locally before the push" rather than disappearing silently.

Concurrency: attach is idempotent. If two webhook workers race, `UNIQUE(repo_id, session_id, item_type)` plus `INSERT ... ON CONFLICT DO UPDATE` on `attached_durable_id` is sufficient.

This requires Wily CLI to reliably emit `renamed` events when slug changes happen — see Phase 3.

## Board Query Behavior

Board should not require a durable row for every live item.

Rendering rules:

- If `live_items.attached_durable_id` is set, render the chip on that durable row.
- Else if `(stage_id, phase_id)` matches a durable row, attach the chip transiently (no DB write).
- Else if `stage_id` alone matches, attach to the Stage row.
- If no durable row matches at all, show the item in a `Local activity awaiting push` section.
- `working` items appear in `Active right now` with a "working" emphasis (e.g., glow or animated chip).
- `active` items appear in `Active right now` with a quieter "alive" treatment.
- `idle` items appear in `Active right now` but de-emphasized; they do not block `Up next`.
- `completed_local` appears in `Needs follow-up` until GitHub sync confirms `done`.
- `blocked_local` appears in `Needs follow-up` until GitHub sync confirms `blocked`.
- `stale` items stay on repo detail for the configured retention window but never appear in dashboard priority sections.

Multi-agent rendering: a Stage with both `codex` and `claude` heartbeats produces two chips on the same row, one per `(actor, agent)`. Last-write-wins is explicitly forbidden — Wily박사 working on his laptop must not erase Right박사's session on hers.

## Wily Watch Behavior

`wily-watch` should show the same local activity reality that Board receives, using local files instead of the network.

Rendering rules:

- Read `.wily/local/live/active/*.json` as the local session registry.
- Show Stage/Phase agent chips directly in the watch pane: `codex working`, `claude active`, `human idle`, `stale`.
- Show local-only Stage/Phase entries immediately, even before they are pushed.
- Keep durable roadmap status visually separate from live session status.
- Never send network events from `wily-watch`; it is a read-only renderer. Event emission remains owned by Wily commands and heartbeat sidecars.

This means a user gets immediate local feedback in `wily-watch` and remote collaborative visibility in Wily Board from the same Wily session lifecycle.

## Wily CLI Behavior

Add a small board client layer in `scripts/wily.py`.

Responsibilities:

- Load board config from env and config files.
- Build live payloads for Stage, Phase, and repo items.
- Generate and persist `session_id` per work session.
- Send signed events best-effort.
- Never fail core Wily commands because Board is down.
- Keep network timeouts short (≤ 2s per request).

Command integration:

- `wily start <id>`:
  - generate `session_id` (ULID)
  - write `.wily/local/live/active/<session-id>.json` with item, actor, agent, started_at, parent_shell_pid
  - send `claimed`
  - fork a detached heartbeat sidecar (default) when `WILY_BOARD_HEARTBEAT=1`; pass `--parent-shell-pid $$`
  - return immediately so the terminal stays free
  - never touch the parent shell's environment
- `wily live-heartbeat <id>`:
  - send `heartbeat` repeatedly (used by the sidecar internally; also exposed for ad-hoc testing)
  - `--agent codex|claude|human`
  - `--interval` (default 30s, min 10s)
  - `--count` (default unlimited; testing uses small N)
  - `--parent-shell-pid` (sidecar mode only)
- `wily live-worked <id>`:
  - send a single `worked` event with optional `--tool`, `--summary`, `--tokens-in`, `--tokens-out`, `--session <sid>`
  - when `--session` is omitted, resolve from the active-registry by cwd + most-recent mtime + agent match
  - returns instantly (< 250ms)
- `wily replan` and any other slug-renaming roadmap command:
  - emit `renamed(session_id, old_item_id, new_item_id)` for every active local session affected
  - update the matching `active/<session-id>.json` `item_id` field in place
- `wily complete <id>`:
  - send `completed_local`
  - remove `.alive`, clear active-registry entry, signal sidecar to exit
- `wily block <id>`:
  - send `blocked_local`; same cleanup
- `wily release <id>` (new, optional):
  - send `released` without marking complete or blocked; same cleanup
- approved local Stage / Phase creation:
  - send `created_local` for the new item, carrying the `session_id` for any in-flight session that authored it

## Agent Work Signals

Heartbeat proves the **process** is alive. It does not prove the **agent** is doing anything. We want Board to distinguish "Codex is actually editing files right now" from "the heartbeat process has been running for 40 minutes while the user went to lunch."

Two complementary channels:

### Channel A: explicit `worked` events from agent hooks

The cheapest, most reliable signal: agents call `wily live-worked` when they do something. We wire this through the agent's existing hook surface, not by sniffing logs.

- **Claude Code**: a `PostToolUse` hook in `~/.claude/settings.json` or repo `.claude/settings.json` runs a small helper that resolves the active session from the session registry and sends a `worked` event. The hook is local and non-blocking; failure does nothing.
- **Codex CLI / IDE**: an equivalent `PostToolUse` hook in `~/.codex/hooks.json` (or repo `.codex/hooks.json` when trusted).
- **Codex Desktop**: see "Codex Desktop Bridge" — App Server subscription replaces the hook when hooks are unreliable.
- **Manual / shell**: humans can call `wily live-worked s21 --summary "ran migration"` to signal meaningful work too.

**Session resolution by file registry, not by environment variable.**

`wily start` cannot mutate the parent shell's environment. Instead it writes `.wily/local/live/active/<session-id>.json` and the hook resolves the active session by reading this directory:

1. Find the nearest ancestor of `cwd` that contains `.wily/local/live/active/`.
2. List all JSON files in that directory.
3. Filter by `agent` matching the calling hook (e.g., the Claude hook ignores `agent=codex-desktop` sessions, and vice versa).
4. Pick the most recently touched file (by `mtime`).
5. Read `session_id`, `item_id`, `actor` from that file and emit the `worked` event.

If no active session matches, the hook silently no-ops — it never blocks the agent's tool call or surfaces an error to the model. Token cost is zero either way; only the hook executor pays.

This design also means **two terminals in the same repo running `wily start` for different stages produce two active files**, and the hook attributes work to whichever was most recently touched. For the typical case (one active stage per repo per agent) this is unambiguous. For multi-stage parallel work, the user can pass `--session <sid>` to `wily live-worked` to be explicit.

### Channel B: optional local activity log drain

For agents that cannot emit hooks but write a structured log, the heartbeat sidecar can tail `.wily/local/live/<session-id>.activity.log` and convert appended lines into `worked` events. This is opt-in via `WILY_BOARD_ACTIVITY_LOG=1` and is **not** the default — file watchers are easy to misconfigure.

### Coalescing

Multiple `worked` events in a short window collapse on the server. Each event still updates `last_worked_at`, but only the most recent payload is retained in `payload_json`. Burst protection: drop events if a session sends more than 60/minute (configurable). This prevents an over-eager hook from drowning Board.

### Status derivation

| Last `worked` (server clock) | Last `heartbeat` (server clock) | Derived `live_status` |
|---|---|---|
| ≤ 90s ago | (any) | `working` |
| > 90s ago | ≤ 60s ago | `active` |
| (none / old) | ≤ 5m ago | `idle` |
| (none / old) | > 5m ago | `stale` |

Windows are server-side config (`LIVE_WORK_SECONDS`, `LIVE_FRESH_SECONDS`, `LIVE_STALE_SECONDS`). Operators can shorten them if Board starts feeling laggy.

## Heartbeat Lifecycle

Use a session-scoped heartbeat, not a global always-running daemon. Default to a **detached sidecar** so `wily start` does not block the user's terminal — they need the same pane for `git`, `wily live-worked`, file edits, and so on. Lifecycle safety comes from **parent-shell PID watch + TTL self-suicide**, not from foreground blocking.

### Default mode: detached sidecar with parent-shell watch

`wily start <id>` (with `WILY_BOARD_HEARTBEAT=1`) does:

1. Generate `session_id`, write the session and active-registry files (see "Runtime files").
2. Send `claimed`.
3. Fork a detached sidecar (`setsid` on POSIX) and **return immediately** so the user's terminal stays free.
4. Print a one-line confirmation: `wily: heartbeat detached for s21 (session SID-W, agent codex)`.

The sidecar receives `--parent-shell-pid $$` from the launching shell and:

- Sends `heartbeat` every 30s.
- Every 10s, checks `os.kill(parent_pid, 0)`. If the parent shell is gone, emits `released` and exits cleanly.
- Carries a hard TTL (`WILY_BOARD_HEARTBEAT_TTL_SECONDS`, default 4h) as a backstop. On expiry, emits `released` and exits.
- Watches `.wily/local/live/<session-id>.alive`. If the file is removed (by `wily live-stop` or `wily complete`/`block`/`release`), exits on the next tick.

This eliminates the orphan-process risk that motivated foreground-by-default, without taking the user's terminal hostage.

### Foreground mode: `--foreground`

`wily start <id> --foreground` runs the heartbeat loop in-process and blocks the shell. Useful for:

- One-shot smoke tests in CI.
- A user who explicitly wants the "session is live" terminal cue.
- Environments where forking is restricted.

Behavior is identical to the detached sidecar minus the fork; SIGINT/SIGTERM cleanly emit `released`.

### Process death detection

The detached sidecar relies on three independent signals so any one failing is non-fatal:

1. **Parent-shell PID poll** — primary. Closes the terminal, sidecar dies within ~10s.
2. **TTL self-suicide** — backstop for the case where the parent shell PID is recycled or unreachable (rare).
3. **`.alive` file watch** — explicit cleanup path. `wily live-stop` and the terminal commands (`complete`/`block`/`release`) remove this file.

### Runtime files

```text
.wily/local/live/
  active/
    <session-id>.json       # session metadata (item, actor, agent, started_at, parent_shell_pid)
  <session-id>.pid          # sidecar PID, both modes
  <session-id>.alive        # liveness marker
  <session-id>.activity.log # optional, opt-in (Channel B)
```

`.wily/local/` is gitignored end-to-end. None of these files are durable state and none are pushed.

The `active/` subdirectory acts as the **session registry**: any tool (hooks, bridges, `wily watch`) that needs to know "what sessions are live in this repo right now" reads the directory. There is no environment variable for this — see "Agent Work Signals" below for why.

### Recovery

If `wily start` is run for an `item_id` that already has an `active/<old-sid>.json` file from a previous run:

- If the old sidecar's PID is alive: refuse to start a second session for the same `(item_id, actor, agent)` tuple unless `--force`. Multiple agents on the same stage are allowed (different `agent`).
- If the old sidecar is dead (PID gone): emit `released` for the orphaned `session_id` so Board clears its chip, then start fresh.

This keeps Board from accumulating ghost chips after laptop sleep + crash.

## Agent Surface Coverage

**Hard constraint:** the `worked` signal must be **token-zero** — i.e., emitted by the agent's runtime, not by the LLM itself. We will not instruct the model to call `wily live-worked`. Every channel below is observed at the runtime/IPC layer; the model burns zero tokens producing the signal.

### Coverage matrix (as of 2026-05)

| Agent surface | `claimed` / `heartbeat` | Token-zero `worked` | Primary mechanism | Notes |
|---|---|---|---|---|
| Claude Code CLI | ✅ via `wily start` detached sidecar | ✅ stable | `PostToolUse` hook in `~/.claude/settings.json` resolves `.wily/local/live/active/*.json` and shells out to `wily live-worked` | Reference hook shipped via `wily hooks install --target claude` |
| Claude Desktop | ✅ if user runs `wily start` in a terminal | ✅ stable when the same hook layer is available | Same registry-resolving `PostToolUse` helper as Claude Code | No parent-shell environment mutation required |
| Codex CLI | ✅ via `wily start` detached sidecar | ✅ stable after hook verification | `PostToolUse` hook in `~/.codex/hooks.json` (project-local `.codex/hooks.json` also accepted when the layer is trusted) | Hook resolves `.wily/local/live/active/*.json` |
| Codex IDE extension (VS Code, JetBrains) | ✅ via `wily start` detached sidecar | ✅ stable after hook verification | Same hook surface as Codex CLI ("CLI and IDE extension share the same configuration layers") | No additional integration work if hook layer is shared |
| **Codex Desktop** | ⚠️ user must run `wily start` separately | ⚠️ via **Codex App Server bridge** (primary) or hooks (fragile right now) | See "Codex Desktop Bridge" below | Hooks have a known regression in recent Desktop alphas (openai/codex #21639). Do not rely on hooks alone. |
| Codex Cloud / web | ❌ out of scope for v1 | ❌ | (no local runtime to observe) | A remote agent reporting back would need its own Board credential path |
| Human terminal | ✅ via `wily start` detached sidecar | ⚠️ manual | User calls `wily live-worked s21 --summary "..."` when they want to mark progress | Used sparingly; humans don't need per-keystroke signals |

The model never produces a `worked` event. All three columns ("claimed/heartbeat", "worked") flow from runtime layers — shell, hook executor, or IPC subscriber.

### Codex Desktop Bridge (primary path)

Codex Desktop ships an **App Server** — a JSON-RPC 2.0 surface that the Desktop process itself uses to drive its UI. It can be exposed over stdio or `ws://127.0.0.1:<port>` and pushes lifecycle notifications including `item/started` and `item/completed` for every tool call, command, file edit, and turn boundary. This is exactly the signal we want, and it never enters the model's context — pure token-zero.

Add a small bridge:

```text
wily codex-bridge start --session s21 --agent codex-desktop [--ws ws://127.0.0.1:4500]
```

Behavior:

- Connects to the local Codex App Server over WebSocket (default) or stdio.
- Subscribes to `thread/*` and `turn/*` lifecycle events.
- Translates each `item/completed` (tool call, command, edit) into a `worked` event sent to Wily Board with the active `session_id`.
- Idle/connection drop: emits no signal — heartbeats from `wily start` keep `active`/`idle` flowing as usual. On reconnect, resumes.
- Coalesces bursts (uses the same 60/min server-side cap).
- Runs as part of the `wily start` detached heartbeat sidecar when `--agent codex-desktop` is selected, so the user does **not** spawn a separate process. Same lifecycle, same parent-shell watch, same TTL, same `.alive` file.

UX:

```sh
wily start s21 --agent codex-desktop
  -> generates session_id
  -> sends claimed + starts detached heartbeat sidecar (as usual)
  -> auto-launches the codex-bridge subscriber against ws://127.0.0.1:4500
  -> Codex Desktop tool calls -> bridge -> Board chip flips to "codex-desktop · working"
```

If the App Server isn't running or refuses the connection, `wily start` continues with `claimed`/`heartbeat` only and prints a one-line warning: `codex-bridge unavailable; live activity will show as 'active' but not 'working'`. The session is not aborted.

### Codex Desktop hooks (secondary, opportunistic)

When the #21639 regression is resolved upstream, `wily hooks install --target codex` will additionally write a `PostToolUse` entry in `~/.codex/hooks.json` that shells out to `wily live-worked` exactly as it does for Codex CLI. Until then, the App Server bridge is the contract. The two channels are **idempotent** on the Board side (event-id dedup), so running both is harmless once both work.

### Fallback: JSONL session-log drain

Codex persists session transcripts as JSONL files when `history.persistence = "save-all"`. As a last-resort fallback (e.g., for a custom Codex build where neither hooks nor App Server are available), `wily codex-bridge start --mode jsonl --path <session-dir>` can tail the JSONL file and emit one `worked` event per tool-call line. This mode is **off by default** because the JSONL schema is not a stable public contract and may shift between Codex releases.

### Investigation log

- Codex Hooks reference confirms `PostToolUse`, `PreToolUse`, `SessionStart`, `Stop`, `PermissionRequest`, `UserPromptSubmit` events and the `~/.codex/hooks.json` location.
- Codex App Server reference confirms stdio and WebSocket (`ws://IP:PORT`) transports and lifecycle event subscription (`item/started`, `item/completed`).
- openai/codex#21639 confirms a current Desktop hook regression — sticky enough to assume hooks alone are not load-bearing for Desktop until further notice.
- We will not link external URLs in this plan; the references above were captured during plan authorship and should be re-verified before Phase 4 implementation.

## Codex and Claude Agent Identity

Do not try to infer agent identity from process names.

Use one of:

- `WILY_BOARD_AGENT=codex`
- `WILY_BOARD_AGENT=claude`
- `wily start s21 --agent codex`
- `wily live-heartbeat s21 --agent claude`

Agent identity is display metadata, not an authorization boundary.

## Operational Concerns

These are the five places this design is most likely to fail in practice. Each one has an explicit answer; if any of these answers change, the plan should be revisited before rollout.

### 1. Sidecar lifecycle

**Risk:** orphan heartbeat processes, ghost chips on Board after a shell crash, PID file leaks. Counter-risk: a foreground loop steals the user's terminal and forces a second pane just to keep working.

**Decision:** default is a **detached sidecar** (terminal stays free), made safe by three layers:

- **Parent-shell PID watch (primary):** sidecar polls `os.kill(parent_pid, 0)` every 10s. Closes the terminal, sidecar emits `released` and exits.
- **TTL self-suicide (backstop):** `WILY_BOARD_HEARTBEAT_TTL_SECONDS` (default 4h). Forgotten processes self-destruct.
- **`.alive` file watch (explicit):** `wily live-stop`, `complete`, `block`, `release` remove this file; sidecar exits on the next tick.

Foreground mode is opt-in via `--foreground` for CI / restricted-fork environments. `wily start` for an `item_id` with a dead sidecar emits `released` for the orphaned session_id before starting fresh.

### 2. Attach key stability (slug renames, replans)

**Risk:** local Stage `s21` becomes `s22` after a replan; durable sync never connects to the local overlay; chip stays stale forever.

**Mitigations:**

- `session_id` is the primary attach key inside Board — but it is **not** written into durable `.wily/` YAML (sessions are local).
- Board maintains the `session_id ↔ current_item_id` mapping from the event stream: `created_local`, then any number of `renamed`, then terminal events. See "Attach Resolution."
- `wily replan` (and any other slug-renaming command) MUST emit a `renamed` event when it changes the slug of a stage that has an active local session.
- Fallback to `(item_type, item_id)` matching against the most recent `created_local` event when no `renamed` chain exists.

### 3. Multi-agent and multi-machine concurrency

**Risk:** Wily박사 and Right박사 (or Codex and Claude on the same machine) both `wily start s21`; one overwrites the other's chip; Board shows a misleading single-actor view.

**Mitigations:**

- Each session has its own `session_id`, so each `(actor, agent, machine)` produces a distinct `live_items` row. No last-write-wins.
- Board renders one chip per `(actor, agent)` pair on the same Stage. The UI must support N>1 chips on a row.
- Agent identity is display metadata only; the same actor can run two agents and both are visible.
- `wily start` does **not** acquire a lock or claim. Coordination is a human-layer concern; Board surfaces collisions instead of preventing them.

### 4. HMAC secret distribution and rotation

**Risk:** every collaborator needs `WILY_BOARD_SECRET` on every machine they work from. There is no answer for how it gets there or how it rotates.

**Mitigations:**

- Document the canonical distribution channel: **1Password shared vault item `wily-board/hmac`**, owned by Wily박사, shared with the R-W-LAB members who need to emit events. (If 1Password is not available, use the org's existing secret-sharing channel — but `.env` over Slack DM is not acceptable.)
- Setup flow:
  1. Pull the secret from 1Password.
  2. Write it to `~/.config/wily/board.env` with `chmod 600`.
  3. Verify with `wily live-heartbeat --count 1 <any-id>`.
- Rotation: Board accepts a comma-separated `WILY_BOARD_SECRETS` env (current + previous) for a 7-day grace window. Rotation cadence: every 90 days, or immediately on suspected compromise.
- `.wily/local/board.env` is gitignored and should never be world-readable.
- A compromised secret only forges live events; it cannot mutate durable state (see Safety §below). This is the explicit blast radius.

### 5. Clocks and idempotency

**Risk:** client clock skew breaks fresh/stale classification; flaky networks cause duplicate events; out-of-order delivery scrambles state.

**Mitigations:**

- **All freshness windows use server clock.** `last_seen_at`, `last_worked_at`, `last_heartbeat_at` are stamped on receipt. `client_time` is recorded for diagnostics only and never compared to thresholds.
- Each event carries an optional `event_id` (client-side ULID). Board dedupes by `(session_id, event_id)` within a 5-minute window using a small in-memory LRU. Duplicates return 200 OK with `dedup=true` so the client treats them as successful.
- Out-of-order delivery is handled by always taking `max(stored, incoming)` for `last_*_at` fields. An older event never moves a timestamp backwards.
- Terminal events (`completed_local`, `blocked_local`, `released`) are sticky: once recorded, a later `heartbeat` for the same session never re-opens it. Reopening requires a new `session_id`.

## Safety

- Live events must never mutate durable roadmap status.
- Board write actions must continue to create PRs rather than pushing directly.
- Secrets stay outside committed `.wily` files; only `.wily/local/` and `~/.config/wily/` hold credentials.
- Heartbeat and worked-event failures are non-blocking.
- Local-only Board entries must be visually provisional (distinct chip styling vs. durable).
- A compromised HMAC secret can forge live activity (annoying) but cannot push commits or mutate roadmap state (contained).

## Relationship To The `heartbeat-freshness` Plan

The earlier `2026-05-16-wily-board-heartbeat-freshness.md` plan builds fresh/stale classification on top of the existing `live_sessions` table (phase-only). This plan **absorbs and supersedes** Tasks 1–3 of that plan:

- Phase 1 below replaces `heartbeat-freshness` Task 1 (Board heartbeat contract) by introducing `live_items` directly. The freshness windows (`LIVE_FRESH_SECONDS`, `LIVE_STALE_SECONDS`) carry over verbatim, plus a new `LIVE_WORK_SECONDS` for the `worked`-event window.
- Phase 2 covers `heartbeat-freshness` Task 3 (rendering) with the expanded rules in "Board Query Behavior."
- The `heartbeat-freshness` Task 2 (`wily live-heartbeat` CLI) is already partially shipped; Phase 3 below extends it rather than rebuilding it.

If `heartbeat-freshness` work has already merged when this plan starts, treat its `live_sessions` rows as legacy: dual-write during Phase 1, switch reads in Phase 2, drop writes in Phase 5.

## Implementation Phases

### Phase 0: Plan reconciliation and surface verification

- Confirm `heartbeat-freshness` plan status. If in-flight, freeze it; if shipped, schedule migration in Phase 1.
- Decide retention windows: defaults of `LIVE_WORK_SECONDS=90`, `LIVE_FRESH_SECONDS=60`, `LIVE_STALE_SECONDS=300`, `LIVE_LOCAL_RETENTION_HOURS=24`, `WILY_BOARD_HEARTBEAT_TTL_SECONDS=14400`.
- Provision the HMAC secret in 1Password and confirm both Wily박사 and Right박사 have working `~/.config/wily/board.env`.
- **Codex Desktop App Server verification gate (blocking for Phase 4b):**
  - Confirm the App Server is reachable on the user's machine, the default listen address/port, and the exact event names for tool-call completion (`item/completed` per current docs but re-verify against the running Desktop build).
  - Capture a 5-minute sample of the event stream during a real Codex Desktop work session and save it under `.wily/local/codex-bridge-samples/` for the bridge test fixture.
  - If the App Server is not exposed by default in the user's Codex Desktop version, document the activation step (config flag, command-line, or settings UI) before bridge implementation starts.
- **Codex CLI hook verification:** confirm `PostToolUse` fires for `Bash`, `apply_patch`, and MCP tool calls in the current Codex CLI build (per openai/codex#16732 the hook surface had gaps; re-test).
- **Claude Code hook verification:** confirm `PostToolUse` payload includes the fields the helper needs (`cwd`, `tool_name`).

### Phase 1: Board live item foundation

- Add `live_items` storage with `session_id`-based unique key and server-clock columns.
- Accept extended live payloads (`session_id`, `event=worked`, `live_status` derivation server-side).
- Backfill compatibility from existing `phase_id` / `stage_id` payloads without `session_id` (anonymous rows, aggressive aging).
- Dedup by `(session_id, event_id)` within a 5-minute window.
- Tests: local-only Stage events, `worked` vs `heartbeat` status derivation, dedup, out-of-order delivery.

### Phase 2: Board rendering for local-only and work-signal activity

- Add `Local activity awaiting push` section.
- Update `Active right now` to split `working` (emphasized), `active`, `idle` chips.
- Render per-`(actor, agent)` chips on a single Stage row.
- Keep durable progress counts unchanged.
- Tests: multi-agent same-stage, working vs active vs idle styling, stale demotion.

### Phase 2b: Wily Watch live session rendering

- Update `wily-watch` and one-shot `wily status` rendering to read `.wily/local/live/active/*.json`.
- Render local agent chips on Stage/Phase rows while keeping durable status separate.
- Render local-only Stage/Phase activity before push.
- Derive local `working`, `active`, `idle`, and `stale` labels from registry timestamps using the same window names as Board.
- Tests: watch output shows Codex/Claude chips, stale sessions are de-emphasized, local-only Stage rows do not change durable progress counts.

### Phase 3: Wily CLI config and event client

- Load `~/.config/wily/board.env` and `.wily/local/board.env`.
- Generate `session_id` per `wily start`; write it to `.wily/local/live/active/<sid>.json` (never to durable YAML).
- Add shared payload builder for stage/phase/repo events.
- Emit `created_local`, `claimed`, `renamed`, `blocked_local`, `completed_local`, `released`.
- Add `wily live-worked` with session resolution by cwd + active-registry mtime + agent filter.
- Make `wily replan` (and any slug-renaming command) emit `renamed` events for every active session it touches.
- Document the session-registry contract (`.wily/local/live/active/`) for hook authors.
- Preserve best-effort behavior; ≤2s network timeouts.

### Phase 4: Heartbeat lifecycle and agent hooks

- Implement detached heartbeat sidecar as the default with parent-shell PID watch, `.alive` marker, PID file, and TTL self-suicide.
- Add `--foreground` mode for CI and restricted-fork environments.
- Add `wily live-stop` and `wily live-stop --all`.
- Crash recovery: detect orphan session files on `wily start`, emit `released` for the dead session.
- Ship `wily hooks install --target claude|codex` that writes a reference `PostToolUse` hook into the appropriate settings file. Both hooks resolve the active session from `.wily/local/live/active/*.json` and call `wily live-worked` (token-zero).
- Add stale behavior tests, multi-agent collision tests, and TTL-expiry tests.

### Phase 4b: Codex Desktop bridge

- Implement `wily codex-bridge` as an App Server WebSocket subscriber (default `ws://127.0.0.1:4500`, configurable).
- Auto-launch the bridge from the detached heartbeat sidecar when `wily start --agent codex-desktop` is used; share the sidecar lifecycle, parent-shell watch, `.alive` marker, and TTL.
- Translate `item/completed` (and equivalent tool-call notifications) into `worked` events with the session's `session_id`.
- Honor the 60/min server burst cap; collapse identical consecutive tool names within a 1s window.
- Graceful degradation: if the App Server is unreachable, log a single warning and continue with heartbeat-only.
- Optional `--mode jsonl --path <session-dir>` fallback for environments without the App Server.
- Tests: bridge translates a synthetic App Server notification stream to correct `worked` payloads; bridge reconnects after a dropped WebSocket; missing App Server does not crash `wily start`.

### Phase 5: Attach resolution and durable sync

- Board maintains `current_item_id` per `live_items` row from the event stream (`created_local` sets it; `renamed` updates it).
- On webhook-driven `.wily/` sync, attach unattached `live_items` rows where `current_item_id` equals the durable slug, falling back to most-recent `created_local` if no `renamed` chain exists.
- Verify `.wily/` parser does NOT need to read `session_id` — durable YAML stays untouched.
- Ensure `wily replan` emits `renamed` events reliably (Phase 3 contract).
- Tests: local Stage → push → attach; replan slug rename → attach still works via the event-stream mapping; durable YAML diff stays clean (no live fields); concurrent webhook workers don't double-attach.

### Phase 6: End-to-end smoke, secret rotation, and operations docs

- Test a local-only Stage before push (Phase 1+2 surface).
- Test Codex heartbeat + `worked` events vs Claude on the same Stage.
- Test stale transition and idle de-emphasis.
- Test push sync attaching the overlay across a replan-rename.
- Test HMAC secret rotation with the `WILY_BOARD_SECRETS` dual-secret grace window.
- Update operations docs: 1Password setup, troubleshooting (no chip showing, ghost chip won't clear, multi-agent rendering), rotation cadence.

## Acceptance Test

Use this end-to-end scenario (covers all five operational concerns plus work signals):

1. Configure live Board env for `R-W-LAB/wily-roadmap` on two machines (Wily박사's laptop, Right박사's laptop), both reading the HMAC secret from 1Password.
2. On Wily박사's laptop, create local Stage `s21` without committing.
3. Wily sends `created_local` with a fresh `session_id` (call it `SID-W`).
4. Board shows `s21` under `Local activity awaiting push`.
5. Run `wily start s21 --agent codex` on Wily박사's laptop. The detached sidecar begins emitting `heartbeat` every 30s while the terminal returns immediately.
6. Board shows a `codex · active` chip on the `s21` overlay.
7. Codex runs a few tool calls; the `PostToolUse` hook fires `wily live-worked s21 --tool Edit` for each. Board flips the chip to `codex · working`.
8. On Right박사's laptop, run `wily start s21 --agent claude` (new `SID-R`). Board now shows **two** chips on the same `s21`: `codex · working` and `claude · active`. Neither erases the other.
9. Right박사's laptop goes to sleep without `wily complete`. After `LIVE_STALE_SECONDS`, Board flips `claude · active` to `claude · stale` and removes it from `Up next` priority.
10. Wily박사 runs `wily replan` and `s21` becomes `s22`. The CLI emits `renamed(SID-W, s21, s22)`. The active-registry file's `item_id` updates in place. **Durable Stage YAML contains no `session_id` field; the diff is clean.**
11. Wily박사 runs `wily complete s22`. The CLI sends `completed_local(SID-W)` and removes `.alive`; the sidecar exits on its next tick. Board shows `completed locally — awaiting push`.
12. Wily박사 commits and pushes `.wily`. The committed diff includes only roadmap state (no live fields).
13. GitHub webhook sync creates the durable `s22` row. Board uses the persisted `live_items.current_item_id` mapping (built from the event stream) to attach the SID-W `live_items` row to the new durable `s22`. Slug rename from `s21` does not break attach.
14. Rotate the HMAC secret: add new secret to `WILY_BOARD_SECRETS` (current,previous), redeploy Board, update 1Password, verify both laptops continue emitting successfully for 7 days, then drop the old secret.

Additional smoke checks:

- Close the launching terminal without running `wily complete/block/release`. Confirm the sidecar notices via parent-shell PID poll within ~10s, emits `released`, and the Board chip transitions to `stale` after `LIVE_STALE_SECONDS`. No PID file is left dangling.
- Force-kill the sidecar itself with SIGKILL. Confirm Board transitions to `stale` after `LIVE_STALE_SECONDS` and `wily start --force` for the same `(item, agent)` works.
- Set `WILY_BOARD_HEARTBEAT_TTL_SECONDS` to a short value (e.g., 60s). Confirm the sidecar self-destructs after the TTL and Board records `released`.
- Run `wily start --foreground s21` in a CI test. Send SIGINT. Confirm `released` is emitted before exit.
- Send the same `heartbeat` twice with identical `event_id` within 5 minutes; confirm Board dedupes.
- **Codex Desktop bridge**: with Codex Desktop running and the App Server listening, `wily start s21 --agent codex-desktop`. Trigger an edit inside Codex Desktop. Confirm the Board chip flips `active` → `working` within ~1s without the model emitting any explicit signal (token-zero proof). Stop Codex Desktop; bridge reconnects on relaunch.
- **Bridge unavailable**: `wily start s21 --agent codex-desktop` with no App Server. Confirm the detached heartbeat sidecar still runs and the warning prints exactly once.

## Open Review Questions

1. Should heartbeat start automatically for every `wily start` when `WILY_BOARD_HEARTBEAT=1`, or should each start require `--heartbeat`?
2. Should local-only Stage creation be emitted only by Wily commands, or should `wily watch` detect local roadmap changes and emit them?
3. Should stale local-only items disappear after a fixed retention window, or stay visible until manually cleared or durable sync catches up?
4. For agent work signals, do we ship the Claude Code `PostToolUse` hook in this repo, in a separate `r-w-lab/wily-hooks` repo, or as a `wily hooks install` subcommand that writes to `~/.claude/settings.json`?
5. Is 4 hours the right default `WILY_BOARD_HEARTBEAT_TTL_SECONDS`, or should it be tighter (e.g., 90 minutes) given typical Wily session length?
6. Should `wily codex-bridge` auto-discover the App Server port (e.g., by reading a Codex Desktop runtime file), or is requiring `--ws ws://127.0.0.1:4500` (with a documented default) acceptable for v1?
7. For Claude Desktop, do we want a parallel "Claude Desktop bridge" using whichever local IPC Claude Desktop exposes (today, Anthropic's MCP runtime), or is the `PostToolUse` hook surface sufficient because Claude Desktop and Claude Code share the same hook layer?

## Recommended Decisions

- Enable automatic heartbeat only when `WILY_BOARD_HEARTBEAT=1`. **Default to detached sidecar with parent-shell PID watch + TTL backstop**, so `wily start` returns immediately and leaves the terminal free. `--foreground` is opt-in for CI/restricted environments.
- **Hooks discover the active session via `.wily/local/live/active/<sid>.json`, not via shell environment variables.** Python cannot mutate the parent shell's env, and even hooks that don't share the shell session can read the file registry.
- **Durable `.wily/` YAML never carries `session_id`.** Board derives `session_id ↔ current_item_id` from the event stream (`created_local` + `renamed`) instead.
- Emit local-only Stage creation from Wily commands first; do not add file watching yet.
- Keep stale local-only items visible on repo detail for 24 hours, but remove them from dashboard priority sections after the stale window.
- **Token-zero is non-negotiable for `worked` signals.** The model never produces them. Every channel — Claude `PostToolUse`, Codex `PostToolUse`, Codex Desktop App Server bridge — observes the runtime, not the conversation.
- Ship `wily hooks install --target claude|codex` to write hook entries. For Codex Desktop, prefer the App Server bridge over hooks until openai/codex#21639 (or successor) is resolved.
- Codex Desktop coverage: **`heartbeat` always, `worked` via App Server bridge when the App Server is reachable, with a graceful no-`worked` fallback.** No JSONL log drain by default.
- Default `WILY_BOARD_HEARTBEAT_TTL_SECONDS=14400` (4h). Revisit after first month of telemetry.
