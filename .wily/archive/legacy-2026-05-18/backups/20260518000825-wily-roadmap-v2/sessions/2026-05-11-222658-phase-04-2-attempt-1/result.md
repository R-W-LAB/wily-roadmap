# Result

Implemented in parallel worker session and integrated by controller.

Summary:
- Hardened lifecycle behavior so `complete` clears stale blocker metadata while tolerating phases without a current session.
- Added lifecycle/status tests for replacement metadata parse/serialize, retry blocker cleanup, block/complete without current sessions, and blocked summary blocker details.
- Updated blocked status summaries to include machine-facing `blocker: ...` detail.
- Updated `$wily-complete` documentation for stale blocker cleanup.

Verification:
- `python3 -m unittest tests.test_wily_cli tests.test_wily_state_summary` passed, 32 tests, 1 skipped.
- `python3 -m unittest discover` passed, 82 tests, 2 skipped.
- `python3 -m py_compile scripts/wily.py scripts/wily_state_summary.py` passed.
