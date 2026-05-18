# Result

Implemented Wily self-update support.

Summary:

- Added `scripts/wily.py update`.
- Added zip install detection with migration guidance.
- Added `--migrate` to clone a sibling git-managed install without deleting the zip install.
- Added git-managed `--check` support with manifest version, local commit, remote commit, and already-current reporting.
- Added dirty working tree refusal before fetch or pull.
- Added `--yes` as the explicit fast-forward-only update path.
- Added `$wily-update` skill and Claude command metadata.
- Added README install/update guidance.
- Added tests that use temporary zip-style installs and local bare git remotes instead of real network access.
