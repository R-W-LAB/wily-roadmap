# Result

Implemented the Board follow-up queue.

- Added `list_review_queue` to collect `completed_local` awaiting-push items, durable `needs_review` phases, local blocker items, and open PR events.
- Dashboard now renders a `Needs follow-up` section with repo/phase links, queue reason chips, live actor chips, and PR links when available.
- Status PR actions now record a `status_pr` event so open PR follow-up can survive page refreshes without a new table.
- Durable `done` phases are excluded from PR queue entries and existing live clear behavior removes completed-local rows after sync confirmation.
