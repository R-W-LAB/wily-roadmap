# Verification

Ran in `/Users/wilycastle/Code/projects/wily-board`:

```sh
uv run pytest tests/test_live_events.py::test_heartbeat_event_updates_existing_session_to_active tests/test_db.py::test_decorate_live_session_freshness_classifies_fresh_and_stale tests/test_config.py -v
```

Result: 3 passed.

```sh
uv run pytest tests/test_live_events.py tests/test_db.py tests/test_config.py
```

Result: 9 passed.

```sh
uv run python -m py_compile app/config.py app/db/repo.py app/live/events.py
```

Result: passed.
