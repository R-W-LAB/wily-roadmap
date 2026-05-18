# Result

Implemented optional runner hooks and `wily-watch` runner progress integration.

- Kept Custom Workflow hooks opt-in in `runners/custom-workflow/hooks/hooks.json`; nothing is installed or activated automatically.
- Added `post_tool_use_verification_capture.py` to append opt-in tool evidence into runner verification artifacts.
- Added `stop_goal_incomplete_guard.py` to inspect Wily phase status, session status, runner recommendation, and autonomy mode for opt-in Stop hooks.
- Added `wily-watch` runner progress display from stable `.wily/sessions/<session>/runner/` status artifacts.
- Updated `wily-watch` documentation to mention compact runner progress rendering.
- Synced updated runtime, hook, and skill files into the local Codex plugin cache.
