# Execution Prompt

Execute Stage s24: S21 realtime Board bridge end-to-end hardening.

Read `agent-handoffs/s21-realtime-board-bridge-requirements.md` first. Implement the bridge so local Board end-to-end verification proves the active Wily session, CustomWorkflow checkpoint status, and Codex `live-worked` hook activity all reach Board API/SSE/UI and Wily status/watch.

Keep durable `.wily` state authoritative. Do not run production smoke, push, deploy, restart services, or write production secrets without explicit approval.
