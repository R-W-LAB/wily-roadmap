# Phase 21-4: Hub and Global MY DESK

## Purpose

Build the first-view dashboard for cross-repo personal work.

## Acceptance

- `/` shows MY DESK first with Working Now, Up Next, and Blocked For Me slots.
- Working/up-next/blocked entries link to the correct repo workspace and phase anchor.
- Shared and Personal repo groups render from `repos.visibility` and login-scoped visibility.
- Repo rows show progress counts, progress bars, live badges, and initialized/uninitialized state.
- Pinned repos persist in `localStorage` and sort first within their visibility group.
- Empty states are rendered for no current work and no next candidate.
- SSE events invalidate the relevant TanStack Query caches without duplicating server-side next logic.
