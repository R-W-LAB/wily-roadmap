# Verification

Ran targeted Board attach tests:

```sh
uv run pytest tests/test_db.py::test_replace_repo_state_clears_matching_completed_local_live_item tests/test_db.py::test_live_item_current_item_id_allows_attach_after_replan_rename
```

Result after implementation: `2 passed`.

Ran full Board tests:

```sh
uv run pytest
```

Result: `59 passed, 23 warnings`.

Ran full Wily CLI tests:

```sh
python3 -m unittest plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest
```

Result: `Ran 84 tests ... OK`.

Ran durable YAML smoke:

```sh
rg -n "session_id|last_seen_at|last_worked_at|live_status" .wily/roadmap.yaml .wily/stages/s22-wily-roadmap-realtime-activity-heartbeat/stage.yaml
```

Result: no runtime live fields; only the Stage 22 task description mentions `session_id`.
