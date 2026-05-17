# Handoff

Stage s24 follows S21 because S21 is now marked done in the current roadmap, but the realtime success criterion was too weak.

Use `agent-handoffs/s21-realtime-board-bridge-requirements.md` as the source of truth. The implementation must distinguish:

- Code or unit-test success.
- Local end-to-end realtime success.
- Production realtime success after explicit approval.

Do not report production realtime success unless an approved production smoke actually proves Board Hub, repo detail, and Wily status/watch are showing the same live checkpoint state.
