# Implementation Plan

1. Add regression tests for Stage-mode Watch rendering:
   - `s22` must render under a `Stage 22` separator/header, not beside `s18` because of dependency depth.
   - compact `wily status` must preserve the current Stage header.
   - ready decomposed Stages with no child Phases must show a missing-decomposition warning.
   - `wily next` must show the first executable child Phase for a ready decomposed Stage.
2. Update Watch rendering so Stage mode orders individual Stage units topologically while labeling by Stage identity.
3. Preserve Stage headers when compacting unfinished Stage-mode output.
4. Add missing-child-Phase detail for decomposed Stages without local child Phase state.
5. Update `wily next` to include the first executable child Phase for decomposed ready Stages and warn when child Phases are missing.
6. Run targeted tests, full Wily CLI tests, and real `wily status` / `wily next` smoke checks.
