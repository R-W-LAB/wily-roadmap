# Wily Board UI Redesign — Design Spec

**Status:** Draft v1
**Authors:** Wily 박사 (kokyuhyun), with Claude
**Date:** 2026-05-16
**Supersedes:** `docs/wily-board-ui-spec.md` (existing calm-dashboard spec) — the information model and theming continuity rules carry forward; the implementation stack and several IA decisions are replaced.

---

## 1. Goal

Wily Board must become a **dashboard for multi-repo personal work**, not a control surface. The user's real pain:

> "협업/개인 여러 repo를 동시에 진행하다 보니, 무엇을 어디까지 했고 어디서부터 다시 시작해야 하는지가 한눈에 보이지 않는다."

Three things must be readable at a glance:

1. **Position** — where the user is across the overall roadmap
2. **Remaining** — how much is left
3. **My work** — what the user is currently holding

All data mutation continues to happen through Wily CLI and Git. The Board is read-only — agents do the work; the Board shows the work.

---

## 2. Information Architecture

Two page modes:

### 2.1 `/` — Hub + Global Workbench

```
┌──────────────────────────────────────────────────────────┐
│ MY DESK  (cross-repo, top of page)                       │
│                                                          │
│ WORKING NOW                                              │
│   ● R-W-LAB/wily-roadmap  21-2 layout    codex   · 3m   │
│   ● R-W-LAB/wily-board    18-3 sync      claude  · 28m  │
│                                                          │
│ UP NEXT  (wily next, sorted cross-repo)                  │
│   ○ R-W-LAB/wily-roadmap  21-3 implement                │
│   ○ kokyuhyun/something    4-1 plan                     │
│   ○ R-W-LAB/wily-board    18-4 reconcile                │
│                                                          │
│ BLOCKED FOR ME  (rendered only when non-empty)           │
│   ⚠ R-W-LAB/wily-board    17-2 needs review             │
├──────────────────────────────────────────────────────────┤
│ SHARED REPOS                                             │
│   ● R-W-LAB/wily-roadmap  16/22  · Right박사 working    │
│   ● R-W-LAB/wily-board     8/12  · idle                 │
│                                                          │
│ PERSONAL REPOS                                           │
│   ● kokyuhyun/something    3/5   · you in_progress      │
└──────────────────────────────────────────────────────────┘
```

- MY DESK is the **first thing the user sees** on entry. Cross-repo by design.
- Repo lists are split into **Shared** and **Personal** groups (existing visibility model in `app/auth` + `repos.visibility`).
- Each repo row shows progress count, progress bar, and a **live badge** (`Right박사 working`, `idle`, `you in_progress`).
- Clicking a row enters the repo workspace.

### 2.2 `/repos/{owner}/{name}` — Repo Workspace

```
┌──────────────────────────────────────────┬──────────────┐
│ DAG STAGE MAP                            │ LOCAL DESK   │
│                                          │ (this repo)  │
│ ┌────┐    ┌──────┐    ┌──────┐           │              │
│ │Done│───▶│ s17  │───▶│ s21  │ working   │ WORKING NOW  │
│ │ 15 │    │needs │    │@codex│           │ ● 21-2       │
│ └────┘    │review│    └──────┘           │              │
│           └──────┘       ▲                │ UP NEXT      │
│             ▲          Right박사 (s17)    │ ○ 21-3       │
│           Right박사                       │ ○ 22-1       │
│                                          │              │
│ Phases inside s21 (htmx-style expansion) │ BLOCKED      │
│   21-1 done                              │ ─            │
│   21-2 working  @codex · 3m              │              │
│   21-3 pending                           │ 📌 Pin repo  │
└──────────────────────────────────────────┴──────────────┘
```

- MAIN: DAG + click-expanded phase list for the selected stage.
- SIDE (Local Desk rail): the same Working / Up Next / Blocked slots, filtered to this repo.
- Both the Global MY DESK and the Local Desk rail consume the **same `wily next` calculation** (computed once on the server, filtered per surface) — no duplicate logic.

---

## 3. Architecture

**Backend:** existing FastAPI service, kept and reduced to a read-only JSON + SSE API.

**Frontend:** new Next.js 15 app (App Router, TypeScript), deployed alongside the existing FastAPI service.

### 3.1 Service split

```
┌──────────────────────┐         ┌──────────────────────┐
│ Next.js 15 (frontend)│  HTTP   │ FastAPI (backend)    │
│ - App Router         │ ──────▶ │ - REST JSON          │
│ - shadcn/ui          │   SSE   │ - SSE /sse/live      │
│ - react-flow         │ ──────▶ │ - Existing auth      │
│ - TanStack Query     │         │ - Wily next compute  │
│ - Framer Motion      │         │ - .wily/ parser      │
│ - Tailwind           │         │ - SQLite             │
└──────────────────────┘         └──────────────────────┘
       (rnwlab.duckdns.org/board)        (same host, internal)
```

- The existing FastAPI service stays. Templates (`board.html`, `repo_detail.html`, `_phase_row.html`) are deleted.
- `app/web/routes.py` is rewritten as JSON endpoints (`/api/repos`, `/api/repos/{owner}/{name}`, `/api/desk`, `/api/sse/live`, etc.).
- `app/actions/*` is **removed entirely** — no more status-change PR creation from the Board.
- Wily CLI's Python parsing, `.wily/` ingest, GitHub sync, and live event endpoint are unchanged.

### 3.2 Auth

The current GitHub OAuth + session-cookie model (in `app/auth/`) is **kept on the FastAPI side**. The Next.js app is configured to forward the session cookie on every request via `credentials: "include"`. CORS allows the frontend origin.

Rationale: Wily CLI and Board share Python code for `.wily/` parsing and the allowed-login policy. Splitting auth across two stacks would duplicate that policy.

### 3.3 Type contract

FastAPI exports an OpenAPI schema. The Next.js build pipeline runs `openapi-typescript` (or `orval`) to generate frontend types. This makes the API contract single-source: backend Pydantic models drive frontend types.

---

## 4. Library Stack

| Concern | Library | Why |
|---|---|---|
| App framework | **Next.js 15 (App Router)** | SSR by default, Server Components for static parts, Route Handlers only where needed (most data fetched directly from FastAPI) |
| Language | **TypeScript** strict | Type safety; openapi-typescript pipeline |
| UI components | **shadcn/ui** | Radix-based, Linear/Vercel/Cal.com tier polish, copy-into-repo (no opaque package) |
| Styling | **Tailwind CSS** | Required by shadcn; design tokens live in `tailwind.config.ts` |
| DAG canvas | **react-flow** (`@xyflow/react`) | Pan/zoom, minimap, custom node renderers, smooth animations out of the box |
| Data fetching | **TanStack Query** | Cache, retry, dedup, SSE-driven invalidation |
| SSE client | **EventSource** (native) + thin custom hook | TanStack Query for state, EventSource for push |
| Animations | **Framer Motion** | Sheet slide, node enter/exit, micro-interactions |
| Charts / progress | **Tremor** | Dashboard-tier progress bars, sparklines if needed |
| Icons | **Lucide-react** | Consistent with current Lucide adoption, tree-shakeable |
| Command palette | **cmdk** | `⌘K` repo/stage quick-jump |
| Toasts | **sonner** | shadcn-recommended; tiny |
| Theme (dark/light) | **next-themes** | Avoids FOUC; integrates with Tailwind `dark:` |
| Date formatting | **`date-fns`** (`formatDistanceToNow` with `ko` locale) | "3분 전" Korean output |
| Markdown (phase task body) | **react-markdown** + `rehype-sanitize` | Safe by default |

**Backend additions:**

| Concern | Library | Why |
|---|---|---|
| SSE | **`sse-starlette`** | De-facto FastAPI SSE; handles keep-alive/close |
| DAG layout (optional, server-side fallback) | **`python-graphviz`** | Only used if we ever need a pre-computed DAG payload; react-flow's `dagre` layout on the client is the primary path |

**Implementation rule (carried into all phases):** "기존에 검증된 OSS가 있으면 우선 채택한다. 새 로직은 (a) OSS가 없거나 (b) OSS가 우리 스택과 호환 안 되거나 (c) 5분 안에 짤 수 있는 trivial일 때만 직접 짠다."

---

## 5. Components

### 5.1 Global MY DESK (`/` page)

- **Three slots**: `WORKING NOW`, `UP NEXT`, `BLOCKED FOR ME`. `BLOCKED FOR ME` slot is hidden when empty; `WORKING NOW` and `UP NEXT` always render with empty-state messaging.
- Each item: `{repo_label} · {phase_id} {phase_title} · {agent} · {relative_time}`.
- Click → repo workspace with `#phase-{id}` anchor, which auto-expands the parent stage's phase list.
- Implementation: shadcn `<Card>` + Framer staggered enter on first paint.

### 5.2 Repo lists (`/` page)

- Two groups: `SHARED REPOS`, `PERSONAL REPOS`. Visibility derived from existing `repos.visibility` column.
- Within each group: pinned repos first (★ icon), then alphabetical.
- Row: `{owner}/{name} · {done}/{total} · {progress bar} · {live badge}`.
- Live badge text examples: `Right박사 working`, `you in_progress`, `idle`, `init 필요` (uninitialized).

### 5.3 Repo switcher (header)

- `<Popover>` with cmdk-backed search. Triggered by header button **and** `⌘K` / `Ctrl+K`.
- Lists all visible repos with the same group split. Recent repos at top.

### 5.4 DAG Stage Map (`/repos/...` page)

- **react-flow** canvas, height clamped to ~60vh on desktop.
- Layout: left-to-right via `dagre` layout helper (shipped with react-flow's example presets).
- Node types:
  - `StageNode`: status dot, stage id (mono), title, optional `@actor·agent` chip when live overlay exists, optional `last worked` micro-label.
  - `DoneBlobNode`: aggregates **all contiguous done stages at the head** of the topological order (no threshold — any consecutive prefix of done stages collapses). Label `Done (N)`. Click expands inline (replaces blob with N stage nodes, re-runs layout with Framer transition). Pinned URL hash `#done=open` keeps it expanded across reloads.
- Edges: thin `--wb-border`, arrowhead small.
- Active stage: thicker border in `--wb-status-prog`; live `working` overlay adds a subtle pulse (`prefers-reduced-motion` disables).
- Pan/zoom: react-flow defaults; double-click resets viewport; `Fit view` button in canvas corner.
- Minimap: bottom-right, small, click-to-pan.

### 5.5 Phase list (under DAG)

- When a stage node is clicked, a `<Sheet side="bottom">` (mobile) or inline panel below the DAG (desktop) expands to show the stage's phases.
- Each phase row: status dot, phase id, title, optional `@owner` chip, `live` chip (`working` / `active` / `idle` / `stale`), `PR open ↗` chip **removed**, no status-change form.
- Phase task body (if present) rendered with `react-markdown` + sanitize.

### 5.6 Local Desk rail (`/repos/...` page)

- shadcn `<Sheet side="right">` with two states:
  - **Expanded (320px)**: full slots, same shape as Global MY DESK but filtered to current repo.
  - **Collapsed (56px)**: vertical icon column. Icons: `⚡` (working count), `✓` (up next count), `⚠` (blocked count, hidden if zero), `📌` (pin).
- Toggle persists in `localStorage` per device.
- **Width-aware default**: viewport ≥1280px → expanded; <1280px → collapsed. **User toggle always wins over auto-default** once toggled.
- Mobile (<600px): rail itself is hidden; replaced by a sticky top `⚡ N` badge that opens a `<Sheet side="bottom">` with the full rail content.

### 5.7 Headline (optional, `/repos/...` page above DAG)

Single line:
```
R-W-LAB · 24/34 stages ━━━━━━━━━━━░░ 6 left
```

- Tremor `<ProgressBar>` with status color
- Optional ETA only if `wily next` cost estimates are present; otherwise omitted.

### 5.8 Attention section (`/repos/...` page, below DAG)

- Shown only when non-empty
- shadcn `<Alert>` style
- Lists blocked stages and `needs_review` items in current repo

### 5.9 Empty states (first-class)

- "현재 들고 있는 작업이 없어요" — when MY DESK `WORKING NOW` is empty
- "다음 후보가 없어요. `$wily-replan`을 고려하세요" — when `UP NEXT` is empty
- "Wily roadmap not initialized" — uninitialized repo
- All rendered with shadcn `<Card>` + muted typography

### 5.10 Toasts

- `sonner` toaster mounted at root
- Used for SSE connection state changes, optimistic UI fallback messages, and copy-to-clipboard confirmations (no data-mutation toasts since there are no mutations)

---

## 6. Data Flow

### 6.1 REST endpoints (FastAPI, JSON)

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/me` | Logged-in user info + partner login |
| GET | `/api/repos` | Visible repos, grouped by visibility |
| GET | `/api/repos/{owner}/{name}` | Repo detail: stages, deps, durable status |
| GET | `/api/repos/{owner}/{name}/phases/{phase_id}` | Phase detail incl. task body |
| GET | `/api/desk` | Cross-repo working / up next / blocked for logged-in user |
| GET | `/api/repos/{owner}/{name}/desk` | Same, filtered to one repo |
| GET | `/sse/live` | Server-Sent Events stream (optional `?repo=owner/name` filter) |

All endpoints require the existing session cookie. CORS allows the Next.js origin only.

### 6.2 SSE events

```
event: live_item.updated
data: { repo, item_type, item_id, actor, agent, live_status, last_worked_at, ... }

event: live_item.cleared
data: { repo, item_type, item_id, actor, agent }

event: durable.synced
data: { repo, last_synced_at }

event: heartbeat
data: { ts }   ← server keep-alive every 25s
```

### 6.3 Frontend subscription model

- Each page mounts one `EventSource` connection
- Events update TanStack Query caches by key (`['desk']`, `['repo', owner, name]`, etc.)
- Re-render triggered by cache invalidation; react-flow consumes the cached repo data
- Connection failure → exponential backoff reconnect (1s → 2s → 5s → 15s); banner shows "Live updates disconnected — retrying" via `sonner`
- Tab/page background → connection paused; on focus return, single full refetch + reconnect

---

## 7. Interaction Model (read-only stance)

### 7.1 Removed

- `_phase_row.html`'s status-change form (`<select>` + Open PR button) and the entire `/actions/phase/status` route
- `app/actions/toggle_status.py` (deleted)
- "Open PR" buttons and `PR open ↗` chips
- Any inline data-mutating control

### 7.2 Kept (UI preferences only, no server data mutation)

- Repo switcher / `⌘K`
- Filter chips (All / Shared / Mine) → URL query param
- Dark / light theme toggle (`next-themes`)
- Rail expanded / collapsed (`localStorage`)
- Search (v1 minimal: repo + stage by id; full-text v2)
- Repo pin ★ (`localStorage` v1; server-side per-user v2)
- Done blob expanded / collapsed (URL hash `#done=open` or in-page state)

### 7.3 Pin mechanism

- Toggle locations: header ☆ on repo workspace page; rail bottom `📌 Pin this repo`
- Storage: `localStorage` keyed `wily.board.pinnedRepos = ["owner/name", ...]`
- Effect: pinned repos appear first within their visibility group on `/`; pinned status reflected in shadcn `<Tooltip>` and ★ icon
- v2: per-user server-side persistence behind same UI

---

## 8. Responsive Behavior

| Width | `/` Hub | `/repos/...` Workspace |
|---|---|---|
| ≥1280 | Single column, max-width 1100px, MY DESK then repo lists | DAG 70% + rail expanded 320px |
| 1024–1280 | Same as above | DAG + rail collapsed 56px (toggleable) |
| 600–1024 | Same as above, denser typography | DAG + top sticky `⚡ N` bar; rail hidden; bar opens bottom sheet |
| <600 | MY DESK vertical, repo lists single column | DAG falls back to vertical stage list; rail replaced by bottom sheet |

- All interactive targets ≥44px hit area (carried from existing ui-spec)
- Sidebar default by width is overridden by user toggle once toggled

---

## 9. Theming Continuity

The current `docs/wily-board-ui-spec.md` §2/§11 rules carry over but are expressed in **Tailwind theme tokens** instead of raw CSS variables:

```ts
// tailwind.config.ts (sketch)
theme: {
  extend: {
    colors: {
      bg:        'hsl(var(--wb-bg))',
      surface:   'hsl(var(--wb-surface))',
      'surface-2': 'hsl(var(--wb-surface-2))',
      border:    'hsl(var(--wb-border))',
      text:      'hsl(var(--wb-text))',
      'text-muted': 'hsl(var(--wb-text-muted))',
      accent:    'hsl(var(--wb-accent))',
      status: {
        done: 'hsl(var(--wb-status-done))',
        prog: 'hsl(var(--wb-status-prog))',
        review: 'hsl(var(--wb-status-review))',
        ready: 'hsl(var(--wb-status-ready))',
        blocked: 'hsl(var(--wb-status-blocked))',
        pending: 'hsl(var(--wb-status-pending))',
        superseded: 'hsl(var(--wb-status-superseded))',
      },
    },
  },
}
```

- CSS variables in `:root` and `[data-theme="dark"]` (next-themes attribute strategy)
- Hex colors **forbidden in components** — must reference Tailwind token names
- Future R-W-LAB lab theme: add `[data-theme="lab"]` with new variable values. Component code unchanged. This matches the existing spec §11 requirement.

---

## 10. Migration Strategy

**Single-deploy cutover at Phase F, parallel development before that.** Reasons: the Board has two users (Wily 박사 + Right 박사), and parallel-running two URLs in production would fragment usage. During development (Phases A–E) the new JSON endpoints sit alongside existing template routes; only at Phase F do template routes go away.

Sequence:

1. **Phase A — API extraction** (Week 1)
   - Add JSON endpoints alongside existing template routes. Existing pages keep working.
   - Generate OpenAPI schema.
2. **Phase B — Next.js scaffold** (Week 1)
   - New repo subdirectory `frontend/` (or sibling repo `wily-board-frontend`, decision in §12).
   - Next.js + Tailwind + shadcn/ui scaffold; `/` and `/repos/[owner]/[name]` empty shells.
   - Authentication flow tested (FastAPI cookie + CORS).
3. **Phase C — Hub page** (Week 1–2)
   - MY DESK + repo lists. Backed by `/api/desk` + `/api/repos`.
   - SSE wired.
4. **Phase D — Repo workspace** (Week 2)
   - DAG via react-flow with Done blob, click-expanded phase list.
   - Local Desk rail.
5. **Phase E — Polish** (Week 2–3)
   - Command palette, toasts, animations, theme toggle, empty states.
   - Responsive validation across breakpoints.
   - Accessibility audit (focus order, screen reader labels, keyboard nav).
6. **Phase F — Cutover** (Week 3)
   - Next.js takes over the root URL; FastAPI template routes deleted; `app/actions/toggle_status.py` removed.
   - One announcement to Right 박사 with the date.
7. **Phase G — Cleanup** (Week 3)
   - Delete `app/web/templates/*.html`, `app/web/static/app.css` (large file deleted), unused Jinja deps.

Feature freeze during cutover: no new Board features in Phase C–F; bugfixes only.

---

## 11. Out of Scope (v2 candidates)

- Server-side pin persistence (per-user)
- Full-text search across phases / task bodies
- Comments / annotations on phases
- Push notifications (browser Notification API)
- Mobile-native client (React Native or PWA install prompt — frontend will be PWA-ready but not aggressively promoted)
- Multi-tenant Board (currently R-W-LAB-only via allowed_github_logins)
- Performance analytics on agents (tokens/time per phase)

---

## 12. Open Questions

1. **Frontend repo layout** — subdirectory `wily-board/frontend/` (monorepo feel, easier ops sync) vs sibling repo `wily-board-frontend` (cleaner separation, allows Vercel deploy). Recommendation: **subdirectory**, with `pnpm` workspaces if needed.
2. **Deployment target for Next.js** — same Docker container/host as FastAPI behind a reverse proxy (boring, single ops surface) vs Vercel (easier preview deploys, paid). Recommendation: **same host** until preview-deploy value is proven.
3. **Connection between Next.js dev server and local FastAPI** — Next.js `rewrites()` proxying `/api/*` to `localhost:8000`. Simple, standard.
4. **i18n** — UI strings stay Korean for now (consistent with current Board). `next-intl` introduced only if/when a second locale is needed.
5. **DAG layout cost** — react-flow with `dagre` runs layout client-side. For very large roadmaps (50+ stages), profile and consider precomputing layout on the server. Defer until empirical issue.
6. **SSE under reverse proxy** — confirm the deployment proxy (nginx? Caddy? duckdns frontend?) doesn't buffer SSE. Add `X-Accel-Buffering: no` header from FastAPI.

---

## 13. Acceptance Criteria

- Wily 박사 opens `/`, sees MY DESK with current working/next/blocked across all visible repos within ~1s of page load
- Clicking a repo opens its workspace with DAG rendered, current active stage visually obvious, Right 박사's active stage visible as a separate live chip
- Local Desk rail on desktop ≥1280 is expanded by default; toggling to collapsed persists across page navigation
- `⌘K` opens the repo switcher, type-ahead works
- SSE updates flip a stage's live chip from `active` to `working` within ~1s of a `worked` event arriving server-side
- Closing the rail and reopening the page from another tab reflects the collapsed state
- Dark mode toggles without FOUC; system preference respected on first visit
- No data-mutating UI exists anywhere in the app (no status select, no Open PR button)
- Lighthouse mobile: Performance ≥85, Accessibility ≥95, Best Practices ≥95
- All interactive controls reachable by Tab in logical order; focus rings visible
