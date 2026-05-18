# Result

Cut FastAPI legacy web routes over to the Next.js-only public surface.

- Deleted `app/web/routes.py`; FastAPI no longer serves `/` or `/repos/{owner}/{name}` HTML template routes.
- Kept FastAPI backend ownership for `/api/*`, `/auth/*`, `/webhooks/*`, `/admin/*`, and `/healthz`.
- Removed `/static/*` from Caddy backend routing because the legacy FastAPI CSS asset was deleted.
- Updated operations docs to describe the read-only Next.js Board route split.
