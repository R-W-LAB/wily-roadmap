# Verification

Ran:

```sh
python3 -m unittest plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_compact_status_keeps_frontier_stage_header_in_stage_mode plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_watch_stage_mode_renders_stage_header_from_stage_id_not_dependency_depth plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_next_reports_first_child_phase_for_ready_decomposed_stage plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_watch_flags_ready_decomposed_stage_with_missing_child_phases
```

Result: `Ran 4 tests ... OK`.

Ran:

```sh
python3 -m unittest plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest
```

Result: `Ran 68 tests ... OK`.

Smoke:

```sh
python3 plugins/wily-roadmap/scripts/wily.py status
```

Result includes `Stage 22` header with Phase rows underneath.

```sh
python3 plugins/wily-roadmap/scripts/wily.py next
```

Result includes `Next phase: 22-1 - Stage/Phase Watch contract guardrail`.

After completing 22-1:

```sh
python3 plugins/wily-roadmap/scripts/wily.py next
```

Result includes `Next phase: 22-2 - Plan reconciliation and surface verification`.
