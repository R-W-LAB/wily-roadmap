# Notes

Implemented the Stage/Phase Watch contract guardrail.

Root cause: Stage mode reused legacy Phase dependency-depth grouping, so `s22` could be placed in the same visual dependency group as `s18`. Compact output also dropped the current Stage header when preserving unfinished lines.

Fixes:

- Stage mode now orders Stage units topologically but renders one visual section per actual Stage.
- Stage headers are generated from the Stage id, e.g. `s22` renders as `Stage 22`.
- compact output preserves the active/frontier Stage header.
- decomposed Stages with missing child Phases render `missing child phases`.
- `wily next` reports the first executable child Phase for a ready decomposed Stage.
