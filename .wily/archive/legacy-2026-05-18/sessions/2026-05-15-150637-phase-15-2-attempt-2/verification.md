# Verification

Executed in `/Users/wilycastle/Code/projects/wily-board`:

```bash
uv run pytest -q
# 16 passed, 2 warnings

uv run python -m py_compile $(find app -name '*.py' -print)
# OK

sh -n deploy/install.sh
# OK
```

Blocked live check:

```bash
ssh -o BatchMode=yes -o ConnectTimeout=10 airman@20.17.177.129 'uname -a'
# ssh: connect to host 20.17.177.129 port 22: Connection refused

nc -vz -w 5 20.17.177.129 22
# nc: connectx to 20.17.177.129 port 22 (tcp) failed: Connection refused

nc -vz -w 5 20.17.177.129 80
# Connection to 20.17.177.129 port 80 [tcp/http] succeeded!

nc -vz -w 5 20.17.177.129 443
# Connection to 20.17.177.129 port 443 [tcp/https] succeeded!
```

Host-only checks not run because SSH is unreachable:

- `systemd-analyze verify /etc/systemd/system/wily-board.service`
- `caddy validate --config /etc/caddy/Caddyfile`
- `curl -fsS https://rnwlab.duckdns.org/healthz`
