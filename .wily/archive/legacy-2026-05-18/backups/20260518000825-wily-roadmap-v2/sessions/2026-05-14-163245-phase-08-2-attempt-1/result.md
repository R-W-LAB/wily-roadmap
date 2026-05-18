# Result

Implemented collaboration-safe Wily state guidance.

- `.gitignore` now allows durable shared Wily state to be tracked:
  - `.wily/roadmap.yaml`
  - `.wily/project.md`
  - `.wily/decisions.md`
  - `.wily/status.md`
  - `.wily/phases/**`
  - `.wily/revisions/**`
- `.wily/sessions/**` remains ignored as local-only execution trace data.
- Added `skills/wily-workflow/references/collaboration-policy.md`.
- Updated Wily workflow/start/complete skills so the plugin guides collaborators to:
  - pull before claiming phase work,
  - treat start as a shared phase claim,
  - commit implementation changes with shared Wily state changes,
  - avoid automatic pushes unless explicitly requested.
- Synced updated skill docs to the local plugin cache so current `$wily-*` skill usage sees the new guidance.
