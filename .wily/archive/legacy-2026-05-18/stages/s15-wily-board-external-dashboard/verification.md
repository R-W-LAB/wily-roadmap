# Verification

Use child Phase verification guidance.

Stage-level acceptance:

- `wily-board` exists as a separate deployable web app or implementation branch.
- The app can ingest `.wily/` state from at least `wily-roadmap`.
- The app can render board/list views on mobile.
- The first write action creates a GitHub PR rather than directly pushing.
- Deployment artifacts fit the Azure 1 GiB RAM constraint.

Current evidence:

- `R-W-LAB/wily-board` commit `458036d` fixes Python package discovery and includes runtime SQL/template/static assets in the deployable wheel.
- `R-W-LAB/wily-board` commit `d54845e` records the live SSH port and makes `deploy/install.sh` preserve the active/custom SSH port in UFW.
- `R-W-LAB/wily-board` commit `f0c639b` makes sync use the GitHub App installation token for private repositories.
- `R-W-LAB/wily-board` commit `cd9fb48` records the live GitHub App installation details in operations docs.
- `R-W-LAB/wily-board` commit `562f5aa` exposes server-side status PR actions from phase cards.
- `uv run pytest -q` in `wily-board` passes: 23 tests.
- Azure VM deployment on `airman@20.17.177.129:5679` completed with systemd `wily-board` active and Caddy active.
- `curl -fsS https://rnwlab.duckdns.org/healthz` returns `{"ok":true}`.
- `deploy/preflight.sh` returns `wily-board preflight ok`.
- Live signed webhook sync returns `{"synced":true}` for `R-W-LAB/wily-roadmap` and `R-W-LAB/Digit`.
- Live signed webhook sync returns `{"synced":false}` for `R-W-LAB/mac2win` and `R-W-LAB/BounceBall` because those default branches do not contain `.wily/roadmap.yaml`.
- Live board status action created `R-W-LAB/wily-roadmap#3` as `app/rnw-board`, changing `.wily/stages/s15-wily-board-external-dashboard/stage.yaml` on a PR branch against `codex/wily-board-stage15`; the smoke PR was closed after verification and the head branch was deleted.
