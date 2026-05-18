# Result

Implemented Phase 16-2: Board live overlay query and UI chips.

- Repo detail phase rows now show provisional live chips such as `airmang working locally`.
- `Active right now` includes phases with live claimed/active/block/complete overlay even when durable status is still pending.
- `Up next` excludes phases that have an uncleared live overlay so claimed local work is not presented as immediately available.
- Durable status dots and progress calculations remain based on committed roadmap state.
