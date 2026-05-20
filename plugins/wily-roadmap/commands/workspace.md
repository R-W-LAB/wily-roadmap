Run the `wily-workspace` skill with arguments: $ARGUMENTS.

Supports `init`, `show-config`, `status`, `next`, and `watch`.

The workspace manifest can be `wily-workspace.yaml` or `.wily-workspace.yaml`.
The manifest is not a source of truth; child repos keep their own `.wily/tasks.yaml`.

`wily workspace status` and `wily workspace next` are read-only aggregate views
and do not claim, start, block, or complete child repo tasks.

`wily workspace init` writes only the manifest and does not create parent `.wily/`.
