# Notes

This is the first phase that should touch multiple existing repositories, so approval boundaries matter.

2026-05-15 live deploy update:

- Wily Board is deployed on the Azure VM reachable via `ssh -p 5679 airman@20.17.177.129`.
- `https://rnwlab.duckdns.org/healthz` returns `{"ok":true}`.
- `GITHUB_OAUTH_CLIENT_ID` and `GITHUB_OAUTH_CLIENT_SECRET` are configured on the server.
- GitHub App values are configured: app ID `3722777`, installation ID `132602517`, private key at `/etc/wily-board/app.pem`.
- `deploy/preflight.sh` returns `wily-board preflight ok`.
- Live signed webhook sync succeeds for `R-W-LAB/wily-roadmap` and `R-W-LAB/Digit`.
- `R-W-LAB/mac2win` and `R-W-LAB/BounceBall` are registered but have no `.wily/roadmap.yaml` on the default branch, so sync returns `false`.
- Live board PR-write smoke created `R-W-LAB/wily-roadmap#3` as `app/rnw-board`, base `codex/wily-board-stage15`, head `wily-board/wily-roadmap-15-7-20260515131404`; the smoke PR was closed after verification and the head branch was deleted.
