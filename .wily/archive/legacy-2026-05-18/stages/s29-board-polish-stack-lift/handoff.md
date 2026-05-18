# s29 Handoff

Stage s29 is complete.

Implemented in `/Users/wilycastle/Code/projects/wily-board`:

- Tailwind CSS and shadcn/ui foundation files, including token mapping for `--wb-*`, `components.json`, `postcss.config.mjs`, `tailwind.config.ts`, `lib/utils.ts`, and local `components/ui/*` primitives.
- shadcn primitive migration for repo switcher Dialog, Local Desk mobile Sheet, Button, Badge, Tooltip, and Alert usage across the existing Board UI.
- TanStack Query provider and SSE key invalidation in `live-refresh.tsx`; `router.refresh()` was removed.
- next-themes provider and theme toggle, date-fns Korean relative time, sanitized markdown phase task rendering, and generated OpenAPI types wired through `frontend/lib/types.ts`.
- FastAPI read endpoints now declare Pydantic response models for repo groups, desk payloads, repo detail, and phase detail so generated frontend types are concrete rather than `unknown`.
- Framer Motion transitions for the Local Desk rail, MY DESK entry list, and stage node layout transitions, with global `prefers-reduced-motion` handling.
- Local dev-session live refresh now treats `WILY_BOARD_DEV_SESSION` as an authenticated live-refresh signal in non-production, matching the existing dev API auth bridge.

Next ready stages after completion:

- `s30`: Wily Board DAG dagre + missing components + mobile.
- `s31`: Heartbeat tail + SSE polish.
