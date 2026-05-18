# Result

Implemented repo visibility storage and config contract.

- Added `PERSONAL_REPOS=owner/name:login` parsing.
- Added `repos.visibility` and `repos.visible_to` with `shared` default.
- `upsert_repo` now stores shared/personal visibility while preserving existing default behavior.
- App startup seeds shared repos from `SYNC_REPOS` and personal repos from `PERSONAL_REPOS`.
- `initialize` safely adds visibility columns for existing SQLite databases.
