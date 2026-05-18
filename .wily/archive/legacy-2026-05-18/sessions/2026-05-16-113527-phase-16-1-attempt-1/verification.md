# Verification

Ran in `/Users/wilycastle/Code/projects/wily-board`:

```sh
uv run pytest tests/test_live_events.py tests/test_db.py tests/test_webhook.py
```

Result: 7 passed.

```sh
uv run python -m py_compile app/db/repo.py app/sync/webhook.py app/live/events.py app/main.py
```

Result: passed.

```sh
uv run pytest
```

Result: 28 passed, 6 warnings. Warnings are existing Starlette TestClient cookie deprecations.

Ran in `/Users/wilycastle/Code/projects/wily-roadmap`:

```sh
python3 plugins/wily-roadmap/scripts/wily.py status
```

Result: rendered Roadmap v17 with s16 and 16-1 in progress.

```sh
python3 -m py_compile plugins/wily-roadmap/scripts/wily.py plugins/wily-roadmap/scripts/wily_state_summary.py
```

Result: passed.
