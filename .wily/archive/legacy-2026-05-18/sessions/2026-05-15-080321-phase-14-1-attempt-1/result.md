# Result

Implemented Stage-first roadmap support without migrating or rewriting existing phase-only roadmaps.

Summary:

- Added `stages:` parsing and serialization alongside the existing `phases:` compatibility path.
- Added Stage readiness, Stage summary output, Stage watch rendering, and direct Stage start sessions.
- Added explicit `decompose-stage` CLI support plus `$wily-decompose-stage` skill metadata.
- Kept decomposition opt-in: `$wily-start <stage-id>` starts the Stage directly and does not create child Phases.
- Added JSON-backed decomposition application that records child Phases and parallel lane write scopes.
- Moved child Phase/lane decomposition state out of shared `roadmap.yaml` and into `.wily/stages/<stage-id>/stage.yaml` to reduce collaboration conflicts.
- Updated `$wily-init` to create Stage-first baseline roadmaps with `stages: []` and repair `.wily/stages/`.
- Updated Wily workflow guidance so Stage is the primary collaboration unit, `owner` and `write_scope` drive safe parallel Stage assignment, and child Phase creation remains explicit.
- Updated `$wily-next` and state summaries to list multiple ready Stage candidates and report whether `write_scope` overlaps.
- Added regression coverage using a `digit`-style phase-only roadmap so shared collaboration state remains compatible.

Verification passed with focused tests, compile checks, full plugin test discovery, and a direct `digit` roadmap status/next check.
