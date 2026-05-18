# Result

Implemented login-scoped repository visibility.

- Added `list_visible_repos` and `repo_visible_to_login`.
- Dashboard filters all repository-derived sections to the logged-in user's visible repo set.
- Direct repo detail URLs return 404 for unauthorized personal repositories.
- Sync/live ingestion remains unfiltered because filtering is applied only in web presentation routes.
