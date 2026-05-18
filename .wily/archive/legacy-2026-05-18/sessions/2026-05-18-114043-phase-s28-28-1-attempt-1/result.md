# Result

Removed the legacy FastAPI/Jinja Board rendering surface from the Wily Board codebase.

- Deleted legacy Jinja templates under `app/web/templates/`.
- Deleted legacy `app/web/static/app.css`.
- Removed FastAPI template route registration from `app/main.py`.
- Removed stale template/static package-data entries from `pyproject.toml`.
