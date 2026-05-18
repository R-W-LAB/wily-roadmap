# Handoff

Stage s23 should run before Stage s21 UI redesign.

The bug being closed: Stage decomposition changes local `.wily` topology immediately, but Board currently sees only committed durable topology or presence-style live activity.

Implementation should preserve the existing local-first and approval-first model:

- Board receives signed provisional draft events.
- Board never writes directly into target repositories.
- Durable GitHub sync remains authoritative.
- Draft topology is cleared when durable `stage.yaml` catches up.
