# Result

Implemented.

- Added Wily roadmap parser support for phase/top-level block scalars (`|`, `|-`, `>`, `>-`).
- Added Wily roadmap parser support for indented block lists such as `depends_on:\n  - "01"`.
- Restricted phase-item detection to the `phases:` list item indentation so nested list items are no longer treated as bogus phases.
- Updated roadmap serialization to emit multi-line strings as YAML block scalars instead of invalid quoted multi-line strings.
- Added regression tests for parser behavior, serialization round-trip, and `wily start` data preservation.
