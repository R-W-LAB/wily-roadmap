# Verification

Completed:

```bash
python3 -m unittest tests.test_wily_watch_ui tests.test_wily_cli
python3 -m unittest discover
python3 -m py_compile scripts/wily.py scripts/wily_watch_ui.py
./wily watch --once --ui ascii
```

Results:

- Focused tests: 86 tests passed, 2 skipped.
- Full unittest discovery: 112 tests passed, 2 skipped.
- Py compile: passed.
- One-shot ASCII watch preview: passed and remained folded/non-interactive by default.

```bash
python3 scripts/wily.py watch --here --ui ascii --interval 0.2
```

TTY smoke result:

- Sent an SGR mouse press on the folded summary row and verified the watch pane expanded completed stages.
- Sent keyboard input ending in `q` and verified the process exited and disabled mouse reporting.
