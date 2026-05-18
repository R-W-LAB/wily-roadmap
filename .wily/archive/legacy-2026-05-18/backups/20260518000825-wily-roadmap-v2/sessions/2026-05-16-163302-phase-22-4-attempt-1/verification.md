# Verification

Ran Board targeted tests in `/Users/wilycastle/Code/projects/wily-board`:

```sh
uv run pytest tests/test_web_routes.py::test_board_renders_item_scoped_stage_activity_awaiting_push tests/test_web_routes.py::test_repo_detail_renders_multiple_live_item_chips_for_same_phase
```

Result after implementation: `2 passed, 2 warnings`.

Ran Wily Watch targeted tests:

```sh
python3 -m unittest plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_watch_renders_local_live_registry_chip_without_changing_progress plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_watch_renders_local_only_live_item_from_registry
```

Result after implementation: `Ran 2 tests ... OK`.

Full Board:

```sh
uv run pytest
```

Result: `57 passed, 23 warnings`.

Full Wily CLI:

```sh
python3 -m unittest plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest
```

Result: `Ran 70 tests ... OK`.
