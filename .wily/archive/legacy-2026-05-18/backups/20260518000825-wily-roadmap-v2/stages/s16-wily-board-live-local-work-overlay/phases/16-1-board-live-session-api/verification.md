# Verification

Run:

```sh
uv run pytest tests/test_live_events.py tests/test_db.py tests/test_webhook.py
```

Also run:

```sh
uv run python -m py_compile app/db/repo.py app/sync/webhook.py app/live/events.py
```
