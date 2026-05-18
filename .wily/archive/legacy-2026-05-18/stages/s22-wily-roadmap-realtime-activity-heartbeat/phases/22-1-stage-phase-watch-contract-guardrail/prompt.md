# Execution Prompt

Implement Phase 22-1: Stage/Phase Watch contract guardrail.

Focus on two failures:

- Decomposed Stages should render as a `Stage N` separator/header with child Phase rows, not as a lone flat Stage item.
- A future ready Stage added with `execution_mode: decomposed` but no child `stage.yaml`/Phases should be caught immediately.
- Stage mode should not reuse legacy Phase dependency-depth grouping in a way that puts `s22` into a visual `Stage 18` group.

Keep changes local-first and scoped to the Wily Roadmap plugin.
