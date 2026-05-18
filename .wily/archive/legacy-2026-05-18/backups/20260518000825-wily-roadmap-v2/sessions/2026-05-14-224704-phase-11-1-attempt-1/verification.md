# Verification

Passed.

- `python3 -m unittest tests.test_wily_cli.ReferenceOnlyWorkflowTest tests.test_wily_cli.WilyCliTest.test_run_creates_external_workflow_handoff_without_bundled_runner tests.test_wily_command_skills.WilyCommandSkillsTest.test_wily_run_documents_external_workflow_handoff_without_completion`
  - Confirmed RED before implementation: failed on existing bundled runner assets and bundled dispatch wording.
- `python3 -m unittest tests.test_wily_command_skills tests.test_wily_cli.ReferenceOnlyWorkflowTest tests.test_wily_cli.WilyCliTest.test_run_creates_external_workflow_handoff_without_bundled_runner tests.test_wily_cli.WilyCliTest.test_run_keeps_runner_and_autonomy_flags_as_external_workflow_metadata`
  - Passed after implementation: 26 tests.
- `python3 -m unittest tests.test_wily_command_skills tests.test_wily_cli tests.test_wily_watch_ui`
  - Passed: 123 tests, 1 skipped.
- `python3 -m unittest discover`
  - Passed: 129 tests, 1 skipped.
- `python3 -m json.tool .codex-plugin/plugin.json >/dev/null`
  - Passed.
- `python3 -m py_compile scripts/wily.py scripts/wily_state_summary.py scripts/wily_watch_ui.py scripts/wily_runner.py`
  - Passed.

Stale wording scan:

rg -n "bundled runner|runners/custom-workflow|custom-workflow|Custom Workflow" .codex-plugin README.md skills commands scripts tests

Remaining matches are test assertions or reference-only/external workflow wording. No live command or skill points to `runners/custom-workflow`.
