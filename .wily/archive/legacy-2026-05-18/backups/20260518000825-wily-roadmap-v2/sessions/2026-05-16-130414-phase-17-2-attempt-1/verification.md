# Verification

Commands run:

- `python3 -m unittest plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_live_heartbeat_requires_phase_id plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_live_heartbeat_requires_board_config plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_live_heartbeat_emits_active_event_with_count_and_note`
  - Passed: 3 tests.
- `python3 -m unittest plugins.wily-roadmap.tests.test_wily_cli`
  - Passed: 79 tests, 1 skipped.
- `python3 -m py_compile plugins/wily-roadmap/scripts/wily.py plugins/wily-roadmap/scripts/wily_state_summary.py`
  - Passed.
