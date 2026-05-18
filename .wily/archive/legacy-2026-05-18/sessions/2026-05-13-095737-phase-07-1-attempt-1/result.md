# Result

Implemented optional GitHub Issues linkage for Wily.

- Added `$wily-issues` as an explicit optional command.
- Default `$wily-issues` mode is read-only: it reports linked issues, unlinked open issues, and suggested roadmap additions.
- Added approved local mutation mode: `issues --add-to-roadmap` creates local Wily phases for unlinked open issues and records `github_issues`, `github_urls`, and `sync_policy: "manual"`.
- Added GitHub Issues policy reference documenting source-of-truth boundaries and future remote-write command split.
- Kept core Wily commands GitHub-free by default.
- Added fixture-based tests with `WILY_ISSUES_JSON` so tests do not require GitHub network access.
