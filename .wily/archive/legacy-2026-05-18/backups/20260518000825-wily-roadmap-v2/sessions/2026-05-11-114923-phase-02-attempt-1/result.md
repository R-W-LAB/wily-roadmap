# Result

Implemented the fast command router policy for Wily command skills.

- `$wily-start` no longer tells the agent to invoke the phase planner while handling the start command.
- `$wily-next` now treats planner adapters as later implementation context, not as command execution work.
- `$wily-complete` clarifies that broad verification is not run by default during completion.
- Shared Wily workflow references now say planner adapters and verification are implementation-phase concerns, not automatic command-skill work.
- Added a command skill invariant test that rejects external planner and broad test-runner instructions in `$wily-*` command skill bodies.

The phase implementation is verified and ready for review.
