# Verification

Ran in `/Users/wilycastle/Code/projects/wily-roadmap`:

```sh
python3 -m unittest plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_start_does_not_emit_board_live_event_without_config plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_start_emits_board_live_event_when_configured plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_complete_emits_board_live_event_when_configured plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_block_emits_board_live_event_with_reason_when_configured
```

Result: 4 tests passed.

```sh
python3 -m unittest plugins.wily-roadmap.tests.test_wily_cli
```

Result: 76 tests passed, 1 skipped.

```sh
python3 -m unittest plugins.wily-roadmap.tests.test_wily_command_skills
```

Result: 24 tests passed.

```sh
python3 -m py_compile plugins/wily-roadmap/scripts/wily.py plugins/wily-roadmap/scripts/wily_state_summary.py
```

Result: passed.
