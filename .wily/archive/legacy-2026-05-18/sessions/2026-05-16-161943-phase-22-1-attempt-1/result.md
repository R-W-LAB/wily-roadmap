# Result

Implemented Phase 22-1.

Changes:

- Added Watch regression tests for Stage-mode headers, dependency-depth grouping, compact status headers, missing child Phases, and `wily next` child Phase hints.
- Updated `wily_watch_ui.py` so Stage mode renders actual Stage sections instead of dependency-depth groups.
- Preserved frontier Stage headers in compact status output.
- Added `missing child phases` / `needs decomposition` detail for decomposed Stages without child Phase rows.
- Updated `wily.py next` to print the first executable child Phase for a ready decomposed Stage.
- Updated `wily.py next` to keep reporting the next ready child Phase after a decomposed Stage is already `in_progress` and the previous child Phase has completed.
