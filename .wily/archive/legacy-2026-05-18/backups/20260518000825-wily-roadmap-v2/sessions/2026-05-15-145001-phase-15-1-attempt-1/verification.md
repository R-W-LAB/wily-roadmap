# Verification

Executed checks in `/Users/wilycastle/Code/projects/wily-board`:

```bash
uv run pytest -q
# 16 passed, 2 warnings

uv run python -m py_compile $(find app -name '*.py' -print)
# OK

sh -n deploy/install.sh
# OK

gh repo create R-W-LAB/wily-board --private --source . --remote origin --push
# Created and pushed https://github.com/R-W-LAB/wily-board
```

Deploy blocker check:

```bash
ssh -o BatchMode=yes -o ConnectTimeout=10 airman@20.17.177.129 'uname -a'
# ssh: connect to host 20.17.177.129 port 22: Connection refused
```
