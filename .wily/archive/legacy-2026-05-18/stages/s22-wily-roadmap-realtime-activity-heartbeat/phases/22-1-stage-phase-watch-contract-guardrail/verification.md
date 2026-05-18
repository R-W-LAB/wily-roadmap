# Verification

- Add or update CLI tests for ready decomposed Stage with no child Phases.
- Verify decomposed Stage output includes a `Stage N` separator/header and child Phase rows.
- Add a regression fixture where `s22` depends on `s20` and confirm Watch does not visually group it under Stage 18 or beside `s18`.
- Verify `wily status` and `wily watch --once` expose the missing decomposition state.
- Verify decomposed Stages with valid child Phases still render Stage header plus Phase rows.
- Verify `wily next` behavior is not misleading for missing child Phases.
