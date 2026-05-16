# Phase 21-5: Repo workspace DAG and Local Desk

## Purpose

Build the repo workspace view around stage position, local desk context, and live activity.

## Acceptance

- `/repos/{owner}/{name}` renders a react-flow DAG with stage nodes and dependency edges.
- Contiguous done stages at the head of the topological order collapse into a Done blob.
- Clicking a stage expands its phases in the desktop inline panel or mobile bottom sheet.
- Phase rows show durable status, owner, task body, and live chips without mutation controls.
- Local Desk rail shows Working Now, Up Next, and Blocked slots filtered to the repo.
- Desktop, tablet, and mobile fallbacks match the responsive behavior in the design spec.
- Repo attention items render when blocked or review work exists.
