# Verification

Run watch-focused tests and the broader suite.

At minimum:

```bash
python3 -m unittest tests.test_wily_cli tests.test_wily_watch_ui
python3 -m unittest discover
```

Manual checks:

- Existing `./wily watch --once --ui ascii` output still works.
- Existing tmux pane behavior remains documented and unchanged unless intentionally revised.
- Any Codex app-friendly mode produces bounded output suitable for a conversation update.

## Evidence

Focused watch and command tests:

```text
python3 -m unittest tests.test_wily_cli tests.test_wily_watch_ui tests.test_wily_command_skills
Ran 133 tests in 3.918s
OK (skipped=1)
```

Full suite:

```text
python3 -m unittest discover
Ran 139 tests in 3.527s
OK (skipped=1)
```

Compile check:

```text
python3 -m py_compile scripts/wily.py scripts/wily_watch_ui.py
exit 0
```

Manual Rich check:

```text
./wily watch --once --ui rich
exit 0
Output used Rich styling and did not print the ASCII fallback message.
```
