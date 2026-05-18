# Result

Implemented `wily run` / `$wily-run` dispatch for the bundled Custom Workflow runner.

- Added `scripts/wily_runner.py` with phase validation, runner/autonomy resolution, session attach/start, runner handoff generation, session runner archive generation, and exact `/goal` command output.
- Added `scripts/wily.py run` as a thin CLI entry point.
- Updated `skills/wily-run/SKILL.md` and `commands/wily-run.md` so the command is documented as state-changing dispatch that never completes a phase.
- Added regression coverage for dispatch artifacts, non-completion behavior, runner/autonomy resolution order, blocked phase rejection, existing-session attach, runner contract files, and command skill documentation.
- Synced the updated runtime files into the local Codex plugin cache.
