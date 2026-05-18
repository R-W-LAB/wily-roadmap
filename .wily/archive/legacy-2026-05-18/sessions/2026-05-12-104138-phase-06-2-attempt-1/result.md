# Result

Implemented Claude Code compatibility guidance for Wily while preserving Codex plugin discovery.

- Added `skills/wily-workflow/references/agent-compatibility.md` with Claude Code command usage, helper invocation, and local-first approval-first boundaries.
- Updated live workflow guidance from Codex-only wording to agent-neutral wording where it affects current execution behavior.
- Broadened `.codex-plugin/plugin.json` descriptions while keeping `skills: "./skills/"`, command default prompts, and the `codex` keyword.
- Added document tests for Claude Code compatibility guidance, platform-neutral live skill wording, and manifest discovery compatibility.
- Saved the detailed implementation plan at `docs/superpowers/plans/2026-05-12-wily-claude-code-compatibility.md`.
