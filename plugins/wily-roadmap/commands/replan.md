Run the `wily-replan` skill with arguments: $ARGUMENTS

When `$ARGUMENTS` is a natural-language work request, create or revise a Roadmap Task for that work. Do not implement the requested work in this command. Commit the task-list draft, then stop after the task draft is committed and report the task id plus next command.

Opt-in drift guard:
- `wily replan install-pre-commit-hook` installs a local git pre-commit hook.
- The hook runs `wily replan drift-guard --from-hook` and never requires a new top-level command.
- When staged files have no active claim or fall outside active claim scope, Wily creates an in-progress `drift: <summary>` task with blank intent and acceptance, then lets the commit continue.
