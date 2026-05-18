# Verification

Run focused tests for roadmap parsing and lifecycle behavior:

```bash
python3 -m unittest tests.test_wily_state_summary tests.test_wily_cli
python3 -m py_compile plugins/wily-roadmap/scripts/wily.py plugins/wily-roadmap/scripts/wily_state_summary.py plugins/wily-roadmap/scripts/wily_watch_ui.py
```

Then run the full suite:

```bash
python3 -m unittest discover
```

Expected:

- old Phase-only roadmaps still parse and render;
- new Stage-level roadmaps can be initialized without premature Phase expansion;
- Stage decomposition creates executable internal Phase work without losing Stage metadata;
- next/status/watch remain readable at both levels.

## Evidence

Focused tests:

```bash
python3 -m unittest plugins/wily-roadmap/tests/test_wily_state_summary.py plugins/wily-roadmap/tests/test_wily_cli.py plugins/wily-roadmap/tests/test_wily_command_skills.py
```

Result: 106 tests ran, OK, 1 skipped.

Compile check:

```bash
python3 -m py_compile plugins/wily-roadmap/scripts/wily.py plugins/wily-roadmap/scripts/wily_state_summary.py plugins/wily-roadmap/scripts/wily_watch_ui.py
```

Result: exit 0.

Full plugin suite:

```bash
cd plugins/wily-roadmap && python3 -m unittest discover
```

Result: 160 tests ran, OK, 2 skipped.

Digit compatibility check:

```bash
python3 /Users/wilycastle/Code/projects/wily-roadmap/plugins/wily-roadmap/scripts/wily.py status
python3 /Users/wilycastle/Code/projects/wily-roadmap/plugins/wily-roadmap/scripts/wily.py next
```

Run from `/Users/wilycastle/Code/projects/digit`. Result: existing phase-only roadmap rendered, and `p01-wily-hit-core` remained the next ready phase.
