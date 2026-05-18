# Result

Blocked before live onboarding and deployment.

Completed before blocker:

- Confirmed target repositories:
  - `R-W-LAB/wily-roadmap`
  - `R-W-LAB/Digit`
  - `R-W-LAB/mac2win`
  - `R-W-LAB/BounceBall`
- Added reusable sync workflow template in `R-W-LAB/wily-board`.
- Opened draft workflow PRs in the four target repositories:
  - `https://github.com/R-W-LAB/wily-roadmap/pull/2`
  - `https://github.com/R-W-LAB/Digit/pull/4`
  - `https://github.com/R-W-LAB/mac2win/pull/187`
  - `https://github.com/R-W-LAB/BounceBall/pull/55`
- Marked those PRs ready and merged them into the default branches.
- Configured `WILY_BOARD_URL=https://rnwlab.duckdns.org` as a GitHub Secret in all four target repositories.
- Generated `WILY_BOARD_SECRET` and `SESSION_SECRET` in a local untracked secret file at `$HOME/.config/wily-board/wily-board.env`.
- Configured `WILY_BOARD_SECRET` as a GitHub Secret in all four target repositories.
- Added `docs/OPERATIONS.md` in `R-W-LAB/wily-board` with live rollout, credential, logging, resync, and blocker instructions.
- Added `deploy/preflight.sh` in `R-W-LAB/wily-board` to validate required env vars, GitHub App key file, active services, and production health after deployment.
- Fixed app session handling so UI and PR actions resolve the GitHub login from the server-side session instead of using the raw cookie value as the actor.
- Pushed current `R-W-LAB/wily-board` `main`.
- Verified local app tests and static checks.

Blockers:

- Azure SSH target is not reachable: `ssh airman@20.17.177.129` returns `Connection refused` on port 22.
- GitHub OAuth App credentials are required before live login can work.
- GitHub App credentials are required before live PR writing can work.
- The same `WILY_BOARD_SECRET` must be copied into the server env file after SSH access is restored.
