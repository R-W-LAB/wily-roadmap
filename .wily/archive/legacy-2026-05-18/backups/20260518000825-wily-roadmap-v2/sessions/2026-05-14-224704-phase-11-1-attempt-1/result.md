# Result

Implemented.

- Removed the live bundled Custom Workflow runner directory from Wily behavior.
- Reworked `$wily-run` so `--runner` is an external workflow label and the command writes a reference-only handoff instead of runner bundle artifacts.
- Updated Wily command/skill guidance and plugin prompt text to describe external workflow handoff behavior.
- Replaced bundled-runner tests with reference-only workflow tests.
