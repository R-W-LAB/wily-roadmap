# Verification

Board targeted red/green:

```sh
uv run pytest tests/test_web_routes.py::test_board_renders_item_scoped_stage_activity_awaiting_push tests/test_web_routes.py::test_repo_detail_renders_multiple_live_item_chips_for_same_phase
```

Red result: failed because Board did not render `live_items`.

Green result: `2 passed, 2 warnings`.

Watch targeted red/green:

```sh
python3 -m unittest plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_watch_renders_local_live_registry_chip_without_changing_progress plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_watch_renders_local_only_live_item_from_registry
```

Red result: failed because Watch ignored `.wily/local/live/active/*.json`.

Green result: `Ran 2 tests ... OK`.

Full Board check:

```sh
uv run pytest
```

Result: `57 passed, 23 warnings`.

Full Wily CLI check:

```sh
python3 -m unittest plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest
```

Result: `Ran 70 tests ... OK`.
