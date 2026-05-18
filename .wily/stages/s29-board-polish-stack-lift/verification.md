# s29 Verification

## 구현 위치

- Repository: `/Users/wilycastle/Code/projects/wily-board`
- Frontend: `frontend/`
- Backend API: read-only response payloads now have Pydantic `response_model` schemas so OpenAPI generation produces concrete frontend types.

## Evidence

- `cd /Users/wilycastle/Code/projects/wily-board/frontend && npm run lint` passed.
- `cd /Users/wilycastle/Code/projects/wily-board/frontend && npm run build` passed.
- `cd /Users/wilycastle/Code/projects/wily-board && uv run pytest` passed: 76 passed, 14 warnings.
- Dependency resolution passed with `npm ls @tanstack/react-query next-themes date-fns react-markdown rehype-sanitize openapi-typescript tailwindcss @radix-ui/react-dialog framer-motion --depth=0`.
- OpenAPI schema generation now emits concrete models for the Board read API:
  - FastAPI routes use `response_model` for repo groups, desk payloads, repo detail, and phase detail.
  - `frontend/lib/api-types.ts` contains `RepoGroupsModel`, `DeskPayloadModel`, `RepoDetailModel`, and `PhaseDetailModel` response schemas.
  - `frontend/lib/types.ts` exports the app-facing type names as aliases of `components["schemas"]` from the generated OpenAPI file.
- Read-only regression search passed with no active app/frontend matches:
  `rg -n "router\\.refresh\\(|useRouter|Open PR|/actions/phase/status|new_status|toggle_status|className=\\\"chip\\\"|className=\\\"icon-button\\\"|dialog-overlay" app frontend --glob '!frontend/node_modules/**' --glob '!frontend/.next/**'`.
- Browser smoke passed through Playwright using the local dev server and a seeded local SQLite DB after the generated type alias change:
  - `/me` renders the personal work surface.
  - Theme toggle changes and survives reload.
  - Repo switcher opens via `Ctrl+K`, lists repos, and closes with Escape.
  - Repo workspace renders the DAG stage map and phase markdown content.
  - Phase detail route renders.
  - Mobile viewport shows the Local Desk Sheet path.
- Post-review fixes were verified:
  - `/me`, `/collab`, and repo workspace surfaces now subscribe to TanStack Query with server-fetched `initialData`, so SSE key invalidation has active subscribers.
  - Next.js API proxy routes now exist for `/api/desk`, `/api/repos/[owner]/[name]`, phase detail, and `/api/sse/live`.
  - `/api/sse/live` proxy forwards browser cookies or non-production `WILY_BOARD_DEV_SESSION` to the FastAPI backend; `curl --max-time 3 http://127.0.0.1:3000/api/sse/live` returned `HTTP/1.1 200 OK` with `text/event-stream` and a heartbeat event under the local dev session.
  - SSE repo payload parsing accepts both `"owner/name"` strings and object payloads.
  - Repo switcher Dialog and Local Desk Sheet now include accessible hidden titles.
  - `rg -n "useQuery\\(|queryKeys\\.repo\\(|queryKeys\\.desk|queryKeys\\.repos|EventSource|repoParts|DialogTitle|SheetTitle" frontend/app frontend/components frontend/lib` confirms query subscribers, invalidation, and accessibility title wiring.
  - `npm ls @playwright/test --depth=0` reports `(empty)` and `rg "stage29-smoke|test-results|playwright-report"` finds no temporary smoke artifacts.

## Notes

- The Browser plugin's in-app browser navigation tool returned invalid URL errors in this session, so the local UI smoke used Playwright with system Chrome as a fallback.
- The temporary smoke spec and Playwright output were removed after verification.
