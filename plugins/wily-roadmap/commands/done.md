Run the `wily-done` skill with arguments: $ARGUMENTS

Scope drift reconciliation:
- By default, `wily done <id>` blocks when files changed since `claim_sha` are outside the task scope.
- Use `--add-scope` to add those files to the current task before marking it done.
- Use `--stub-drift` to create or reuse a `drift: <summary>` helper task and then mark the current task done.
