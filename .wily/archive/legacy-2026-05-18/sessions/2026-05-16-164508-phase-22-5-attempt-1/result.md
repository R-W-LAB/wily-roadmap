# Result

Completed Phase 22-5.

Implemented Wily CLI live session identity and heartbeat lifecycle:

- repo-local/user/env Board config loading
- active registry files in `.wily/local/live/active`
- `.alive` and `.pid` lifecycle files
- detached heartbeat sidecar spawn
- parent-shell PID release handling
- `release` command
- registry cleanup on `complete` and `block`
- orphan registry recovery on `start`
