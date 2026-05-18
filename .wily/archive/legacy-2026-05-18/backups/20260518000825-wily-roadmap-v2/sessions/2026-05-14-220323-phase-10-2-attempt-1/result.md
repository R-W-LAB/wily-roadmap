# Result

Implemented the Codex app watch strategy.

Summary:

- `./wily watch` now keeps tmux behavior when already inside tmux.
- Outside tmux, an interactive terminal now runs the live dashboard directly, so Codex app users can open a side terminal and run `./wily watch`.
- Non-interactive processes outside tmux now get bounded guidance instead of an accidental long-running loop.
- Rich remains the preferred default through `--ui auto`; after `./wily watch --install-ui`, Wily uses `.venv-watch` and renders the styled dashboard.
- Updated `$wily-watch`, Claude command metadata, and README guidance to document the side-terminal Codex app workflow.
