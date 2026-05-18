# Phase 24-1: Board live config, diagnostics, and hook contract

Define and verify the local live bridge setup contract.

Acceptance:

- Repo-local `.wily/board.json` is supported and protected from accidental commit.
- `wily board check` reports URL, repo, actor, hook, Board reachability, and signature readiness while redacting secrets.
- Missing config or hook setup is visible in active Wily surfaces when realtime Board visibility is expected.
- Codex hook installation is inspectable, reversible, and verified.
