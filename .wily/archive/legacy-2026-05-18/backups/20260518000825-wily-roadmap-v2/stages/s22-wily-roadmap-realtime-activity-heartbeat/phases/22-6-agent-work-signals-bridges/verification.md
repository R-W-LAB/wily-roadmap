# Verification

Targeted red/green:

```sh
python3 -m unittest plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_live_worked_resolves_active_session_and_updates_registry plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_live_worked_from_hook_without_active_session_is_non_blocking plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_hooks_install_codex_writes_post_tool_use_command plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_hooks_install_claude_writes_post_tool_use_command plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_codex_bridge_fixture_converts_item_completed_to_worked plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_codex_bridge_missing_fixture_degrades_to_heartbeat_only
```

Red result: failed before implementation because `live-worked`, `hooks`, and `codex-bridge` did not exist.

Green result: `Ran 6 tests ... OK`.

Full Wily CLI check:

```sh
python3 -m unittest plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest
```

Result: `Ran 84 tests ... OK`.
