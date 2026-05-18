# Result

Removed Board write actions and the GitHub PR status mutator from Wily Board.

- Deleted `app/actions/routes.py`, `app/actions/toggle_status.py`, and `app/actions/pr_writer.py`.
- Removed PR writer setup and mutable action state from `app/main.py`.
- Preserved GitHub App installation-token behavior for repository sync by moving it into `app/sync/github_app.py`.
- Replaced legacy action tests with route absence and sync-token tests.
