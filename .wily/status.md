# Wily Status

Roadmap version 16 has Stage s15 complete.

Current baseline:
- `R-W-LAB/wily-board` exists as a private repository and has the local FastAPI/SQLite/htmx implementation pushed.
- Child Phases 15-1 through 15-6 are implemented. Phase 15-2 is now deployed on the Azure VM via SSH port 5679.
- Live board health is up: `https://rnwlab.duckdns.org/healthz` returns `{"ok":true}` and `/` redirects to `/auth/github/start`.
- `R-W-LAB/wily-board` now includes `docs/OPERATIONS.md`, `deploy/preflight.sh`, GitHub App token based private repo sync, and server-side status PR actions exposed from phase cards.
- Child Phase 15-7 merged workflow PRs for all four initial repositories and configured `WILY_BOARD_URL` plus `WILY_BOARD_SECRET` secrets.
- Server `deploy/preflight.sh` returns `wily-board preflight ok`.
- Live signed webhook sync succeeds for `R-W-LAB/wily-roadmap` and `R-W-LAB/Digit`; `R-W-LAB/mac2win` and `R-W-LAB/BounceBall` are registered but have no `.wily/roadmap.yaml` on the default branch.
- Live board PR-write smoke created `R-W-LAB/wily-roadmap#3` as `app/rnw-board`, targeting `codex/wily-board-stage15`; the smoke PR was then closed and its head branch deleted.
- Stage s14 is done; child Phase 14-2 remains superseded by user request.

Next action:
- No Stage 15 implementation action remains.
- Workflow PRs are merged on default branches:
  - `R-W-LAB/wily-roadmap#2`
  - `R-W-LAB/Digit#4`
  - `R-W-LAB/mac2win#187`
  - `R-W-LAB/BounceBall#55`
