# Phase 21-3: Next.js scaffold and auth bridge

## Purpose

Create the frontend application skeleton and prove it can authenticate through the existing FastAPI session model.

## Acceptance

- `wily-board/frontend/` contains a Next.js 15 App Router app with strict TypeScript.
- Tailwind and shadcn/ui are configured with Wily Board theme tokens.
- OpenAPI-generated API types are wired into the frontend build.
- Local rewrites proxy API/SSE requests to FastAPI during development.
- The app forwards the session cookie and renders authenticated hub and repo page shells.
- Unauthenticated users follow the existing GitHub OAuth flow.
