# Handoff

Stage s22 is ready.

Start with Phase 22-1. The first patch is a Wily plugin guardrail: a ready decomposed Stage must not silently render as a lone flat Stage in Watch when child Phases are missing.

The key product outcome is that Wily Roadmap becomes the realtime operating layer for personal and shared work:

- `wily-watch` shows local Stage/Phase activity immediately.
- Wily Board shows the same work remotely through signed live events.
- Codex and Claude activity appears as heartbeat plus token-zero `worked` signals.
- Local-only work is clearly provisional until `.wily` is pushed and GitHub sync attaches it.

Stage s21 UI redesign is intentionally held until this foundation exists.
