# Result

Deployment artifacts are implemented and pushed in `R-W-LAB/wily-board`.

Implemented:

- Ubuntu bootstrap script for app user, directories, dependencies, firewall, fail2ban, swap, virtualenv install, Caddyfile install, and systemd unit install.
- Caddy reverse proxy config for `rnwlab.duckdns.org`.
- systemd service running `uvicorn app.main:create_app --factory` with one worker.
- GitHub Actions sync workflow template that signs the full JSON payload.

Blocked:

- Live Azure bootstrap cannot run because `ssh airman@20.17.177.129` returns `Connection refused` on port 22.
- Unblock requirement: make SSH on `20.17.177.129:22` reachable from this machine, or provide the correct host/port/user.
