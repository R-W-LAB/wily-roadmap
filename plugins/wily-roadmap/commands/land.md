---
description: Commit, push, and land a completed Wily phase
argument-hint: '<stage-id>/<phase-id>'
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion
---

Run the `wily-land` skill to publish completed Wily work.

This command is explicit remote repository work. Use it only after the phase has been completed and the user wants the work committed, pushed, and either fast-forward landed with `--direct` or opened as a PR with `--pr`.

Phase id (required):

$ARGUMENTS
