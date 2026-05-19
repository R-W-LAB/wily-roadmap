Run the `wily-init` skill with arguments: $ARGUMENTS

`wily init commit` also attempts a best-effort `wily-agent` registry update
when local agent config includes a Board repo. Registration failures never fail
init; run `wily agent register` manually if a warning is printed.
