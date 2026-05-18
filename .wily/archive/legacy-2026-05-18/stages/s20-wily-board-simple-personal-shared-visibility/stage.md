# s20: Wily Board simple personal and shared repo visibility

## Purpose

Let Wily Board show shared collaboration repositories to both users while showing personal repositories only to their owner, without adding a full workspace model.

## Confirmed Product Decision

Use the simple two-user model:

- `visibility = shared`, `visible_to = null`: visible to both `airmang` and `Julirsia`.
- `visibility = personal`, `visible_to = airmang`: visible only to `airmang`.

This means `Julirsia` sees the collaboration organization repositories only, while `airmang` sees those shared repositories plus personal repositories.

## Child Phases

- 20-1 Repo visibility fields and config contract [pending]
- 20-2 Login-scoped repo filtering and access control [pending]
- 20-3 Simple Shared and Mine Board filters [pending]
- 20-4 Personal repo onboarding docs and verification [pending]
