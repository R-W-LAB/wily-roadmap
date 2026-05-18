# Verification

Completed prerequisite migration/watch-display checks:

```bash
python3 -m unittest plugins/wily-roadmap/tests/test_wily_watch_ui.py -k stage_first_summary_counts_done_stages_not_child_phases
# OK, 1 test

python3 -m unittest plugins/wily-roadmap/tests/test_wily_watch_ui.py
# OK, 56 tests, 1 skipped

python3 -m unittest plugins/wily-roadmap/tests/test_wily_cli.py plugins/wily-roadmap/tests/test_wily_watch_ui.py
# OK, 128 tests, 2 skipped

python3 -m unittest plugins/wily-roadmap/tests/test_wily_state_summary.py plugins/wily-roadmap/tests/test_wily_command_skills.py
# OK, 36 tests

python3 -m py_compile plugins/wily-roadmap/scripts/wily.py plugins/wily-roadmap/scripts/wily_state_summary.py plugins/wily-roadmap/scripts/wily_watch_ui.py
# OK

cd plugins/wily-roadmap && python3 -m unittest discover
# OK, 164 tests, 2 skipped

python3 plugins/wily-roadmap/scripts/wily.py status
# shows v14 Stage-first roadmap, 13 stages done, s14 with child 14-1/14-2

python3 plugins/wily-roadmap/scripts/wily.py next
# shows active stage s14 and active phase 14-2

python3 /Users/wilycastle/Code/projects/wily-roadmap/plugins/wily-roadmap/scripts/wily.py status
# from /Users/wilycastle/Code/projects/digit: OK, legacy/stage migrated digit roadmap still renders

python3 /Users/wilycastle/Code/projects/wily-roadmap/plugins/wily-roadmap/scripts/wily.py next
# from /Users/wilycastle/Code/projects/digit: OK, next stage remains p04-right-layers-elevator
```

Remaining 14-2 verification after implementation:

```bash
python3 -m unittest plugins/wily-roadmap/tests/test_wily_cli.py plugins/wily-roadmap/tests/test_wily_watch_ui.py
python3 -m py_compile plugins/wily-roadmap/scripts/wily.py plugins/wily-roadmap/scripts/wily_watch_ui.py
cd plugins/wily-roadmap && python3 -m unittest discover
```

Expected:

- dry-run pane command uses the intended bottom horizontal split mode for smartphone/Codex app watch;
- compact horizontal layout fits short pane heights;
- existing side-pane watch behavior remains covered.
