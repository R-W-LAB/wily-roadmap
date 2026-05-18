# Verification

Expected checks:

```bash
python3 -m pytest
curl -fsS https://<host>/healthz
```

Live repository checks require approved credentials and should record exact repositories and PR URLs.

Recorded merged workflow PRs:

```text
R-W-LAB/wily-roadmap#2  MERGED 2026-05-15T06:17:10Z
R-W-LAB/Digit#4         MERGED 2026-05-15T06:17:15Z
R-W-LAB/mac2win#187     MERGED 2026-05-15T06:17:21Z
R-W-LAB/BounceBall#55   MERGED 2026-05-15T06:17:26Z
```

Remaining live checks are blocked by SSH and credentials:

```bash
curl -fsS https://rnwlab.duckdns.org/healthz
# not expected to pass until Azure deploy completes
```

Repository secret checks:

```text
R-W-LAB/wily-roadmap  WILY_BOARD_URL set, WILY_BOARD_SECRET set
R-W-LAB/Digit         WILY_BOARD_URL set, WILY_BOARD_SECRET set
R-W-LAB/mac2win       WILY_BOARD_URL set, WILY_BOARD_SECRET set
R-W-LAB/BounceBall    WILY_BOARD_URL set, WILY_BOARD_SECRET set
```

Latest `R-W-LAB/wily-board` verification:

```bash
uv run pytest -q
# 19 passed, 3 warnings

uv run python -m py_compile $(find app -name '*.py' -print)
# OK
```

Default branch workflow file checks:

```text
R-W-LAB/wily-roadmap  .github/workflows/wily-board-sync.yml present
R-W-LAB/Digit         .github/workflows/wily-board-sync.yml present
R-W-LAB/mac2win       .github/workflows/wily-board-sync.yml present
R-W-LAB/BounceBall    .github/workflows/wily-board-sync.yml present
```
