# Execution Prompt

Execute Stage s21: Wily Board UI redesign.

Keep the work focused on the existing Board app plus its new frontend subdirectory. Preserve the current local-first and approval-first model: committed `.wily` state remains authoritative, live overlay state remains provisional, and the redesigned Board must not directly mutate roadmap data.

Start with the selected child Phase, not the whole Stage. Before implementation, verify the child Phase's target files and acceptance criteria. The design contract is `docs/superpowers/specs/2026-05-16-wily-board-ui-redesign-design.md`.

Revision 24 adds a required checkpoint bridge before continuing the frontend cutover: CustomWorkflow `agent-handoffs/*-status.md` checkpoints must attach to the current Wily Phase as live runner overlay so Roadmap, Watch, and Board can show current checkpoint progress without treating every checkpoint as durable roadmap state.
