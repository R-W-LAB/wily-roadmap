# Verification

Ran targeted lifecycle tests:

```sh
python3 -m unittest plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_board_live_config_loads_repo_local_untracked_file plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_start_writes_live_active_registry_without_board_config plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_start_spawns_detached_heartbeat_when_enabled plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_complete_cleans_live_registry_and_alive_marker plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_live_heartbeat_writes_pid_file_and_updates_registry_session plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_live_heartbeat_releases_when_parent_shell_is_gone plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_release_cleans_live_registry_without_changing_phase_status plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_start_recovers_orphan_live_registry_without_alive_marker
```

Result after implementation: `Ran 8 tests ... OK`.

Ran full Wily CLI tests:

```sh
python3 -m unittest plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest
```

Result: `Ran 78 tests ... OK`.
