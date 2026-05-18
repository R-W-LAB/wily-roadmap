# Verification

Ran:

```bash
python3 -m json.tool .codex-plugin/plugin.json
python3 -m unittest tests.test_wily_command_skills
python3 -m unittest tests.test_wily_cli tests.test_wily_state_summary tests.test_wily_watch_ui
python3 -m py_compile scripts/wily.py scripts/wily_state_summary.py scripts/wily_watch_ui.py
python3 scripts/wily.py status
python3 scripts/wily.py watch --once --ui ascii
python3 -m unittest tests.test_wily_command_skills.WilyCommandSkillsTest.test_workflow_docs_describe_status_pane_not_old_phase_flow
python3 -m unittest discover
rg -n "TODO|TBD|placeholder|old external workflow" .codex-plugin skills scripts tests docs
```

Results:
- JSON validation: pass.
- `tests.test_wily_command_skills`: 11 tests pass.
- CLI/state/watch targeted tests: 77 tests pass, 2 skipped.
- py_compile: pass.
- status/watch manual inspection: both render `Wily Roadmap` pane output.
- workflow-doc regression test: pass after live-doc update.
- full discover: 89 tests pass, 2 skipped.
- blocked-string search: only historical plan/spec references and release-audit search text remain; no live plugin drift requiring another edit.
