# Wily Status

Roadmap version 16 has Stage s15 in a blocked state.

Current baseline:
- `R-W-LAB/wily-board` exists as a private repository and has the local FastAPI/SQLite/htmx implementation pushed.
- Child Phases 15-1 through 15-6 are implemented. Phase 15-2 is now deployed on the Azure VM via SSH port 5679.
- Live board health is up: `https://rnwlab.duckdns.org/healthz` returns `{"ok":true}` and `/` redirects to `/auth/github/start`.
- `R-W-LAB/wily-board` now includes `docs/OPERATIONS.md`, `deploy/preflight.sh`, and GitHub App token based private repo sync.
- Child Phase 15-7 merged workflow PRs for all four initial repositories and configured `WILY_BOARD_URL` plus `WILY_BOARD_SECRET` secrets.
- Server `deploy/preflight.sh` returns `wily-board preflight ok`.
- Live signed webhook sync succeeds for `R-W-LAB/wily-roadmap` and `R-W-LAB/Digit`; `R-W-LAB/mac2win` and `R-W-LAB/BounceBall` are registered but have no `.wily/roadmap.yaml` on the default branch.
- Stage s15 remains blocked only on a real board PR-write smoke against an appropriate Wily state branch.
- Stage s14 is done; child Phase 14-2 remains superseded by user request.

Next action:
- Run the final PR-write smoke from the board against a branch that contains the target Stage/Phase state.
- Workflow PRs are merged on default branches:
  - `R-W-LAB/wily-roadmap#2`
  - `R-W-LAB/Digit#4`
  - `R-W-LAB/mac2win#187`
  - `R-W-LAB/BounceBall#55`
