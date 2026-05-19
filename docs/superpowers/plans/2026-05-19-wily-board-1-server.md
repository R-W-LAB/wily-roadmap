# Wily Board v3 — Plan 1: Server Foundation + Agent Ingest API

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `wily-board` server skeleton (FastAPI + SQLite + GitHub OAuth) and the `/agent/*` ingest API so a hand-crafted `curl` payload from any machine creates correct DB rows. No UI cards and no real-time SSE in this plan — only the foundation that Plans 2 and 3 build on.

**Architecture:** Single Python service. FastAPI app (`app/`) with sync endpoints. SQLite (stdlib `sqlite3`) is the single source of truth — schema is created from `app/db/schema.sql` and applied by a small migrator. Auth: GitHub OAuth → secure HTTP-only session cookie → R-W-LAB org allowlist gate. Agent endpoints use a per-machine bearer token; the one-time code that exchanges for a token is minted via an authenticated web endpoint (web UI is a stub login + "Add machine" button in this plan). Deploy artifacts (Caddyfile, systemd unit, install.sh, backup.sh) ship in `deploy/` and the README documents bootstrap.

**Tech Stack:**
- Python 3.12
- FastAPI + uvicorn (sync defs, 1 worker)
- SQLite (stdlib `sqlite3`)
- Jinja2 templates (FastAPI integration)
- `httpx` for outbound HTTP (GitHub API) and `httpx.ASGITransport` for FastAPI test client
- `pytest` + `pytest-asyncio` (only where needed)
- `ruff` (lint + format)
- `uv` for env and dependency management (lockfile committed)
- Caddy 2 / systemd / Debian-flavoured Linux for production

**Spec:** `docs/superpowers/specs/2026-05-19-wily-board-v3-design.md`. Plan 1 implements all of §6 (DB), §7 ingest flow up to but not including SSE broadcast, §8 API endpoints `/agent/*` and `/auth/github/*`, and a minimal `/web/login` + `/web/machines` shell. Plan 1 also delivers §11/§12 deploy/migration mechanics. UI cards/SSE/realtime (§7 SSE event + §9 dashboard) are deferred to Plan 3.

---

## File Structure

```
wily-board/                              # NEW REPO (sibling of wily-roadmap)
  .gitignore
  pyproject.toml
  uv.lock
  README.md
  app/
    __init__.py
    main.py                              # FastAPI app + lifespan
    config.py                            # env settings (pydantic-settings)
    db/
      __init__.py
      schema.sql                         # full v3 schema (spec §6)
      migrations.py                      # apply_schema(conn) + future migrations
      repo.py                            # thin CRUD helpers
    parsers/
      __init__.py
      wily_state.py                      # validate + normalize agent payload
    merge/
      __init__.py
      policy.py                          # apply_snapshot(conn, parsed) → diff summary
    auth/
      __init__.py
      sessions.py                        # cookie-based session middleware
      github_oauth.py                    # /auth/github/{start,callback}
      allowlist.py                       # org-membership check (mockable)
    api/
      __init__.py
      agent.py                           # /agent/register, /agent/snapshot, /agent/heartbeat
      machines.py                        # /web/machines (one-time code mint, web-auth)
    web/
      __init__.py
      routes.py                          # /, /login (minimal shell)
      templates/
        base.html
        login.html
        machines.html                    # "Add machine" + token display once
      static/
        pico.min.css                     # vendored
        app.css                          # ~50 lines, layout shell only
  deploy/
    Caddyfile
    wily-board.service
    install.sh
    backup.sh
  tests/
    __init__.py
    conftest.py                          # in-memory DB + TestClient + fixtures
    contracts/
      agent_v1.json                      # canonical example payload
    test_db_schema.py
    test_db_repo.py
    test_parsers_wily_state.py
    test_merge_policy_tasks.py
    test_merge_policy_append.py
    test_auth_sessions.py
    test_auth_github_oauth.py
    test_auth_allowlist.py
    test_api_machines.py
    test_api_agent_register.py
    test_api_agent_snapshot.py
    test_api_agent_heartbeat.py
    test_smoke_end_to_end.py
```

**Repo creation note:** Plan starts from an empty directory `wily-board/` next to `wily-roadmap/`. If the legacy v2 repo already exists at `R-W-LAB/wily-board`, create a `feat/v3-rewrite` branch from an *empty* tree (`git checkout --orphan feat/v3-rewrite && git rm -rf .`) so legacy history is preserved on `main`. The plan does not depend on whether v2 history exists — both paths land at the same scaffold.

---

## Task 1: Repo scaffold + tooling

**Files:**
- Create: `wily-board/.gitignore`
- Create: `wily-board/pyproject.toml`
- Create: `wily-board/README.md`
- Create: `wily-board/app/__init__.py`
- Create: `wily-board/tests/__init__.py`

- [ ] **Step 1: Initialize repo and Python env**

Run:
```bash
mkdir -p ~/Code/projects/wily-board && cd ~/Code/projects/wily-board
git init
uv init --python 3.12 --no-readme
```

- [ ] **Step 2: Write `.gitignore`**

Create `wily-board/.gitignore`:
```
__pycache__/
*.pyc
.pytest_cache/
.ruff_cache/
.venv/
.env
*.sqlite
*.sqlite-journal
deploy/local/
```

- [ ] **Step 3: Write `pyproject.toml`**

Create `wily-board/pyproject.toml`:
```toml
[project]
name = "wily-board"
version = "0.1.0"
description = "Read-only web board for Wily Roadmap v3"
requires-python = ">=3.12"
dependencies = [
  "fastapi>=0.110",
  "uvicorn[standard]>=0.27",
  "jinja2>=3.1",
  "httpx>=0.27",
  "pydantic>=2.6",
  "pydantic-settings>=2.2",
  "itsdangerous>=2.1",
]

[project.optional-dependencies]
dev = [
  "pytest>=8.0",
  "pytest-asyncio>=0.23",
  "ruff>=0.4",
]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
```

- [ ] **Step 4: Write minimal README**

Create `wily-board/README.md`:
```markdown
# Wily Board

Read-only web board for Wily Roadmap v3.

See `docs/superpowers/specs/2026-05-19-wily-board-v3-design.md` (in the wily-roadmap repo) for the design spec.

## Development

```
uv sync --extra dev
uv run uvicorn app.main:app --reload
uv run pytest
```
```

- [ ] **Step 5: Touch package `__init__.py` files and verify install**

Create empty `wily-board/app/__init__.py` and `wily-board/tests/__init__.py`. Then:
```bash
uv sync --extra dev
```
Expected: exits 0, `.venv/` created, no errors.

- [ ] **Step 6: Commit**

```bash
git add .gitignore pyproject.toml uv.lock README.md app tests
git commit -m "chore: scaffold wily-board v3 package"
```

---

## Task 2: Config module

**Files:**
- Create: `wily-board/app/config.py`
- Create: `wily-board/tests/test_config.py`

- [ ] **Step 1: Write failing test**

Create `wily-board/tests/test_config.py`:
```python
import os

from app.config import Settings


def test_settings_reads_environment(monkeypatch):
    monkeypatch.setenv("WB_HOST", "127.0.0.1")
    monkeypatch.setenv("WB_PORT", "9000")
    monkeypatch.setenv("WB_SQLITE_PATH", "/tmp/board.sqlite")
    monkeypatch.setenv("WB_SESSION_SECRET", "x" * 32)
    monkeypatch.setenv("WB_GITHUB_CLIENT_ID", "gh-id")
    monkeypatch.setenv("WB_GITHUB_CLIENT_SECRET", "gh-secret")
    monkeypatch.setenv("WB_GITHUB_ORG", "R-W-LAB")
    monkeypatch.setenv("WB_BASE_URL", "https://board.example")

    s = Settings()
    assert s.host == "127.0.0.1"
    assert s.port == 9000
    assert s.sqlite_path == "/tmp/board.sqlite"
    assert s.github_org == "R-W-LAB"
    assert s.base_url == "https://board.example"


def test_settings_requires_session_secret(monkeypatch):
    monkeypatch.delenv("WB_SESSION_SECRET", raising=False)
    monkeypatch.setenv("WB_GITHUB_CLIENT_ID", "gh-id")
    monkeypatch.setenv("WB_GITHUB_CLIENT_SECRET", "gh-secret")
    monkeypatch.setenv("WB_GITHUB_ORG", "R-W-LAB")
    monkeypatch.setenv("WB_BASE_URL", "https://board.example")
    try:
        Settings()
    except Exception:
        return
    raise AssertionError("Settings should fail without WB_SESSION_SECRET")
```

- [ ] **Step 2: Run test, expect fail**

```bash
uv run pytest tests/test_config.py -v
```
Expected: ImportError / no module `app.config`.

- [ ] **Step 3: Implement `app/config.py`**

Create `wily-board/app/config.py`:
```python
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="WB_", env_file=".env", extra="ignore")

    host: str = "127.0.0.1"
    port: int = 8080
    sqlite_path: str = "var/board.sqlite"
    session_secret: str = Field(min_length=32)
    session_cookie_name: str = "wb_session"
    session_max_age_seconds: int = 60 * 60 * 24 * 14
    github_client_id: str
    github_client_secret: str
    github_org: str
    base_url: str
    agent_token_pepper: str = "wily-board-agent-v3"
```

- [ ] **Step 4: Run tests, expect pass**

```bash
uv run pytest tests/test_config.py -v
```
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add app/config.py tests/test_config.py
git commit -m "feat(config): env-driven settings"
```

---

## Task 3: SQLite schema + migrator

**Files:**
- Create: `wily-board/app/db/__init__.py`
- Create: `wily-board/app/db/schema.sql`
- Create: `wily-board/app/db/migrations.py`
- Create: `wily-board/tests/test_db_schema.py`
- Create: `wily-board/tests/conftest.py`

- [ ] **Step 1: Write conftest with in-memory DB fixture**

Create `wily-board/tests/conftest.py`:
```python
import sqlite3

import pytest

from app.db.migrations import apply_schema


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys = ON")
    apply_schema(c)
    yield c
    c.close()
```

- [ ] **Step 2: Write failing schema test**

Create `wily-board/tests/test_db_schema.py`:
```python
EXPECTED_TABLES = {
    "users", "machines", "projects", "project_machines",
    "task_snapshots", "tasks", "task_progress", "cp_events",
    "project_actors", "task_results", "observed_commits",
    "agent_events", "actor_presence", "oauth_sessions",
}


def test_schema_creates_all_tables(conn):
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()
    names = {row["name"] for row in rows}
    missing = EXPECTED_TABLES - names
    assert not missing, f"missing tables: {sorted(missing)}"


def test_tasks_has_parallel_columns(conn):
    cols = {row["name"] for row in conn.execute("PRAGMA table_info(tasks)")}
    assert {"parallel_lane", "priority", "capacity_hint"} <= cols


def test_cp_events_primary_key(conn):
    conn.execute(
        "INSERT INTO cp_events(project_id, task_id, ts, actor, cp, event, ingest_machine) "
        "VALUES ('p','T1','2026-05-19T00:00:00Z','wily','plan','start','m1')"
    )
    # second identical insert must be ignored (PK collision)
    try:
        conn.execute(
            "INSERT INTO cp_events(project_id, task_id, ts, actor, cp, event, ingest_machine) "
            "VALUES ('p','T1','2026-05-19T00:00:00Z','wily','plan','start','m1')"
        )
    except Exception:
        return
    raise AssertionError("duplicate cp_events insert should fail PK constraint")
```

- [ ] **Step 3: Run tests, expect fail**

```bash
uv run pytest tests/test_db_schema.py -v
```
Expected: ImportError on `app.db.migrations`.

- [ ] **Step 4: Write `app/db/schema.sql`**

Create `wily-board/app/db/schema.sql` mirroring spec §6 exactly. Include every CREATE TABLE statement from the spec: `users`, `machines`, `projects`, `project_machines`, `task_snapshots`, `tasks` (with `parallel_lane`, `priority`, `capacity_hint`), `task_progress`, `cp_events`, `project_actors`, `task_results`, `observed_commits`, `agent_events`, `actor_presence`, `oauth_sessions`.

```sql
-- wily-board v3 schema. Source of truth: spec §6.
CREATE TABLE IF NOT EXISTS users (
  github_id      INTEGER PRIMARY KEY,
  login          TEXT NOT NULL,
  display        TEXT,
  avatar_url     TEXT,
  allowlist_role TEXT NOT NULL,
  created_at     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS machines (
  id           TEXT PRIMARY KEY,
  user_id      INTEGER NOT NULL REFERENCES users(github_id),
  hostname     TEXT NOT NULL,
  token_hash   TEXT NOT NULL UNIQUE,
  created_at   TEXT NOT NULL,
  last_seen    TEXT
);

CREATE TABLE IF NOT EXISTS projects (
  id              TEXT PRIMARY KEY,
  remote_url      TEXT NOT NULL,
  title           TEXT,
  mode_hint       TEXT,
  first_seen_at   TEXT NOT NULL,
  last_update_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS project_machines (
  project_id    TEXT NOT NULL REFERENCES projects(id),
  machine_id    TEXT NOT NULL REFERENCES machines(id),
  local_path    TEXT NOT NULL,
  registered_at TEXT NOT NULL,
  PRIMARY KEY (project_id, machine_id)
);

CREATE TABLE IF NOT EXISTS task_snapshots (
  project_id   TEXT NOT NULL,
  machine_id   TEXT NOT NULL,
  snapshot_sha TEXT NOT NULL,
  tasks_json   TEXT NOT NULL,
  project_md   TEXT,
  actors_json  TEXT,
  updated_at   TEXT NOT NULL,
  PRIMARY KEY (project_id, machine_id)
);

CREATE TABLE IF NOT EXISTS tasks (
  project_id              TEXT NOT NULL,
  task_id                 TEXT NOT NULL,
  title                   TEXT NOT NULL,
  intent                  TEXT,
  acceptance              TEXT,
  scope_json              TEXT,
  depends_on_json         TEXT,
  status                  TEXT NOT NULL,
  assignee                TEXT,
  actor                   TEXT,
  claim_sha               TEXT,
  claim_at                TEXT,
  done_at                 TEXT,
  blocker                 TEXT,
  parallel_lane           TEXT,
  priority                INTEGER,
  capacity_hint           INTEGER,
  last_updated_by_machine TEXT NOT NULL,
  last_updated_at         TEXT NOT NULL,
  PRIMARY KEY (project_id, task_id)
);

CREATE TABLE IF NOT EXISTS task_progress (
  project_id    TEXT NOT NULL,
  task_id       TEXT NOT NULL,
  cp_done       INTEGER NOT NULL DEFAULT 0,
  cp_total      INTEGER NOT NULL DEFAULT 0,
  current_cp    TEXT,
  cp_names_json TEXT,
  updated_at    TEXT NOT NULL,
  PRIMARY KEY (project_id, task_id)
);

CREATE TABLE IF NOT EXISTS cp_events (
  project_id     TEXT NOT NULL,
  task_id        TEXT NOT NULL,
  ts             TEXT NOT NULL,
  actor          TEXT NOT NULL,
  cp             TEXT NOT NULL,
  event          TEXT NOT NULL,
  note           TEXT,
  ingest_machine TEXT NOT NULL,
  PRIMARY KEY (project_id, task_id, ts, cp, event, actor)
);

CREATE TABLE IF NOT EXISTS project_actors (
  project_id      TEXT NOT NULL,
  actor_id        TEXT NOT NULL,
  display         TEXT,
  capacity        INTEGER NOT NULL DEFAULT 1,
  git_emails_json TEXT,
  git_names_json  TEXT,
  PRIMARY KEY (project_id, actor_id)
);

CREATE TABLE IF NOT EXISTS task_results (
  project_id TEXT NOT NULL,
  task_id    TEXT NOT NULL,
  body       TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (project_id, task_id)
);

CREATE TABLE IF NOT EXISTS observed_commits (
  project_id      TEXT NOT NULL,
  sha             TEXT NOT NULL,
  author          TEXT,
  committed_at    TEXT,
  subject         TEXT,
  guessed_task_id TEXT,
  PRIMARY KEY (project_id, sha)
);

CREATE TABLE IF NOT EXISTS agent_events (
  id          INTEGER PRIMARY KEY,
  machine_id  TEXT NOT NULL,
  project_id  TEXT,
  type        TEXT NOT NULL,
  payload     TEXT,
  created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS actor_presence (
  user_id            INTEGER NOT NULL,
  machine_id         TEXT NOT NULL,
  current_project_id TEXT,
  current_task_id    TEXT,
  last_seen          TEXT NOT NULL,
  PRIMARY KEY (user_id, machine_id)
);

CREATE TABLE IF NOT EXISTS oauth_sessions (
  sid        TEXT PRIMARY KEY,
  user_id    INTEGER NOT NULL,
  expires_at TEXT NOT NULL
);
```

- [ ] **Step 5: Write `app/db/migrations.py`**

Create `wily-board/app/db/migrations.py`:
```python
from importlib.resources import files
from sqlite3 import Connection


def apply_schema(conn: Connection) -> None:
    sql = files("app.db").joinpath("schema.sql").read_text(encoding="utf-8")
    conn.executescript(sql)
    conn.commit()
```

Create empty `wily-board/app/db/__init__.py`.

- [ ] **Step 6: Run tests, expect pass**

```bash
uv run pytest tests/test_db_schema.py -v
```
Expected: 3 passed.

- [ ] **Step 7: Commit**

```bash
git add app/db tests/conftest.py tests/test_db_schema.py
git commit -m "feat(db): v3 schema + migrator"
```

---

## Task 4: DB repo helpers

**Files:**
- Create: `wily-board/app/db/repo.py`
- Create: `wily-board/tests/test_db_repo.py`

- [ ] **Step 1: Write failing repo test**

Create `wily-board/tests/test_db_repo.py`:
```python
from app.db import repo


def test_upsert_user_and_get(conn):
    repo.upsert_user(conn, github_id=1, login="wily", display="Wily 박사",
                     avatar_url="https://...", role="wily",
                     created_at="2026-05-19T00:00:00Z")
    u = repo.get_user(conn, 1)
    assert u["login"] == "wily"
    assert u["allowlist_role"] == "wily"


def test_create_machine_and_lookup_by_token_hash(conn):
    repo.upsert_user(conn, github_id=1, login="wily", display="", avatar_url="",
                     role="wily", created_at="2026-05-19T00:00:00Z")
    repo.create_machine(conn, machine_id="m1", user_id=1, hostname="laptop",
                        token_hash="hash1", created_at="2026-05-19T00:00:00Z")
    m = repo.find_machine_by_token_hash(conn, "hash1")
    assert m["id"] == "m1"
    assert m["user_id"] == 1


def test_upsert_project(conn):
    repo.upsert_project(conn, project_id="p1", remote_url="git@x:y/z.git",
                        title="demo", mode_hint="solo",
                        first_seen_at="2026-05-19T00:00:00Z",
                        last_update_at="2026-05-19T00:00:00Z")
    p = repo.get_project(conn, "p1")
    assert p["title"] == "demo"
```

- [ ] **Step 2: Run, expect fail**

```bash
uv run pytest tests/test_db_repo.py -v
```
Expected: ImportError on `app.db.repo`.

- [ ] **Step 3: Implement `app/db/repo.py`**

Create `wily-board/app/db/repo.py`:
```python
from sqlite3 import Connection
from typing import Any


def upsert_user(conn: Connection, *, github_id: int, login: str, display: str,
                avatar_url: str, role: str, created_at: str) -> None:
    conn.execute(
        """INSERT INTO users(github_id, login, display, avatar_url, allowlist_role, created_at)
           VALUES (?, ?, ?, ?, ?, ?)
           ON CONFLICT(github_id) DO UPDATE SET
             login=excluded.login,
             display=excluded.display,
             avatar_url=excluded.avatar_url,
             allowlist_role=excluded.allowlist_role""",
        (github_id, login, display, avatar_url, role, created_at),
    )
    conn.commit()


def get_user(conn: Connection, github_id: int) -> dict[str, Any] | None:
    row = conn.execute("SELECT * FROM users WHERE github_id=?", (github_id,)).fetchone()
    return dict(row) if row else None


def create_machine(conn: Connection, *, machine_id: str, user_id: int,
                   hostname: str, token_hash: str, created_at: str) -> None:
    conn.execute(
        "INSERT INTO machines(id, user_id, hostname, token_hash, created_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (machine_id, user_id, hostname, token_hash, created_at),
    )
    conn.commit()


def find_machine_by_token_hash(conn: Connection, token_hash: str) -> dict[str, Any] | None:
    row = conn.execute(
        "SELECT * FROM machines WHERE token_hash=?", (token_hash,)
    ).fetchone()
    return dict(row) if row else None


def upsert_project(conn: Connection, *, project_id: str, remote_url: str,
                   title: str, mode_hint: str | None, first_seen_at: str,
                   last_update_at: str) -> None:
    conn.execute(
        """INSERT INTO projects(id, remote_url, title, mode_hint, first_seen_at, last_update_at)
           VALUES (?, ?, ?, ?, ?, ?)
           ON CONFLICT(id) DO UPDATE SET
             title=excluded.title,
             mode_hint=excluded.mode_hint,
             last_update_at=excluded.last_update_at""",
        (project_id, remote_url, title, mode_hint, first_seen_at, last_update_at),
    )
    conn.commit()


def get_project(conn: Connection, project_id: str) -> dict[str, Any] | None:
    row = conn.execute("SELECT * FROM projects WHERE id=?", (project_id,)).fetchone()
    return dict(row) if row else None
```

- [ ] **Step 4: Run, expect pass**

```bash
uv run pytest tests/test_db_repo.py -v
```
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add app/db/repo.py tests/test_db_repo.py
git commit -m "feat(db): repo helpers for users/machines/projects"
```

---

## Task 5: Snapshot payload parser

**Files:**
- Create: `wily-board/app/parsers/__init__.py`
- Create: `wily-board/app/parsers/wily_state.py`
- Create: `wily-board/tests/contracts/agent_v1.json`
- Create: `wily-board/tests/test_parsers_wily_state.py`

- [ ] **Step 1: Write canonical contract fixture**

Create `wily-board/tests/contracts/agent_v1.json` mirroring spec §8 example. Include parallel fields, cp_events, observed_commits, actors with capacity, task_results.

```json
{
  "project_id": "9c1c1f0e7e9f6e3b7a1c4d4f7b8b9d2e8a3c2d1f",
  "snapshot_sha": "REPLACE_AT_RUNTIME",
  "remote_url": "git@github.com:R-W-LAB/wily-roadmap.git",
  "title": "wily-roadmap v3: 로컬 우선 에이전트 작업을 위한 프로젝트 및 태스크 관리자",
  "mode_hint": "solo",
  "tasks": [
    {
      "id": "T04",
      "title": "병렬 watch",
      "intent": "병렬 가능 작업 시각화",
      "acceptance": "watch 출력에 lane/priority/capacity 반영",
      "scope": ["plugins/wily-roadmap/scripts/wily/ui/watch_render.py"],
      "depends_on": [],
      "status": "done",
      "assignee": "wily",
      "actor": "wily",
      "claim_sha": "c114abd",
      "claim_at": "2026-05-18T14:43:10Z",
      "done_at": "2026-05-18T14:55:08Z",
      "blocker": null,
      "parallel_lane": "ui",
      "priority": 1,
      "capacity_hint": 2
    }
  ],
  "actors": {
    "wily": {
      "display": "Wily 박사",
      "git_author_emails": ["kokyuhyun@goedu.kr"],
      "git_author_names": [],
      "capacity": 2
    }
  },
  "task_progress": {
    "T04": {"done": 5, "total": 5, "current_cp": null,
            "cp_names": ["Execution package","RED tests","Implementation","Documentation","Final verification"]}
  },
  "cp_events": {
    "T04": [
      {"ts":"2026-05-18T14:55:21Z","actor":"wily","cp":"Execution package","event":"start"},
      {"ts":"2026-05-18T14:55:21Z","actor":"wily","cp":"Execution package","event":"done"}
    ]
  },
  "task_results": {"T04": "# T04: 병렬 watch — done\n\n- actor: wily\n"},
  "observed_commits": [
    {"sha":"296db49","author":"kokyuhyun","committed_at":"2026-05-18T23:58:12+09:00",
     "subject":"T04: add advanced parallel watch model","guessed_task_id":"T04"}
  ],
  "project_md": "# wily-roadmap v3: ...",
  "client_version": "wily-agent/0.1.0",
  "captured_at": "2026-05-19T03:14:15Z"
}
```

- [ ] **Step 2: Write failing parser test**

Create `wily-board/tests/test_parsers_wily_state.py`:
```python
import json
from pathlib import Path

import pytest

from app.parsers.wily_state import ParseError, parse_snapshot

FIXTURE = Path(__file__).parent / "contracts" / "agent_v1.json"


def load() -> dict:
    return json.loads(FIXTURE.read_text())


def test_parse_snapshot_returns_normalized_structure():
    payload = load()
    parsed = parse_snapshot(payload)
    assert parsed.project_id == payload["project_id"]
    assert parsed.tasks[0].id == "T04"
    assert parsed.tasks[0].parallel_lane == "ui"
    assert parsed.actors["wily"].capacity == 2
    assert parsed.task_progress["T04"].total == 5
    assert parsed.cp_events["T04"][0].cp == "Execution package"
    assert parsed.observed_commits[0].sha == "296db49"
    assert parsed.task_results["T04"].startswith("# T04")


def test_parse_snapshot_rejects_missing_required():
    payload = load()
    del payload["project_id"]
    with pytest.raises(ParseError):
        parse_snapshot(payload)


def test_parse_snapshot_rejects_oversize_project_md():
    payload = load()
    payload["project_md"] = "x" * (64 * 1024 + 1)
    with pytest.raises(ParseError):
        parse_snapshot(payload)


def test_parse_snapshot_idempotent_sha():
    from app.parsers.wily_state import canonical_sha
    payload = load()
    one = canonical_sha(payload)
    payload2 = {**payload, "captured_at": "2027-01-01T00:00:00Z"}
    two = canonical_sha(payload2)
    assert one == two, "captured_at must not affect sha"
```

- [ ] **Step 3: Run, expect fail**

```bash
uv run pytest tests/test_parsers_wily_state.py -v
```
Expected: import error.

- [ ] **Step 4: Implement parser**

Create `wily-board/app/parsers/__init__.py` (empty) and `wily-board/app/parsers/wily_state.py`:
```python
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

MAX_PROJECT_MD = 64 * 1024


class ParseError(ValueError):
    pass


@dataclass
class TaskRecord:
    id: str
    title: str
    intent: str | None
    acceptance: str | None
    scope: list[str]
    depends_on: list[str]
    status: str
    assignee: str | None
    actor: str | None
    claim_sha: str | None
    claim_at: str | None
    done_at: str | None
    blocker: str | None
    parallel_lane: str | None
    priority: int | None
    capacity_hint: int | None


@dataclass
class ActorRecord:
    display: str
    git_author_emails: list[str]
    git_author_names: list[str]
    capacity: int


@dataclass
class ProgressRecord:
    done: int
    total: int
    current_cp: str | None
    cp_names: list[str]


@dataclass
class CpEventRecord:
    ts: str
    actor: str
    cp: str
    event: str
    note: str | None = None


@dataclass
class CommitRecord:
    sha: str
    author: str | None
    committed_at: str | None
    subject: str | None
    guessed_task_id: str | None


@dataclass
class Snapshot:
    project_id: str
    snapshot_sha: str
    remote_url: str
    title: str
    mode_hint: str | None
    tasks: list[TaskRecord]
    actors: dict[str, ActorRecord]
    task_progress: dict[str, ProgressRecord]
    cp_events: dict[str, list[CpEventRecord]]
    task_results: dict[str, str]
    observed_commits: list[CommitRecord]
    project_md: str | None
    client_version: str
    captured_at: str


REQUIRED_KEYS = {
    "project_id", "snapshot_sha", "remote_url", "title", "tasks",
    "actors", "captured_at", "client_version",
}


def parse_snapshot(payload: dict[str, Any]) -> Snapshot:
    missing = REQUIRED_KEYS - payload.keys()
    if missing:
        raise ParseError(f"missing required keys: {sorted(missing)}")
    project_md = payload.get("project_md")
    if project_md is not None and len(project_md) > MAX_PROJECT_MD:
        raise ParseError("project_md exceeds 64KB cap")
    return Snapshot(
        project_id=payload["project_id"],
        snapshot_sha=payload["snapshot_sha"],
        remote_url=payload["remote_url"],
        title=payload["title"],
        mode_hint=payload.get("mode_hint"),
        tasks=[_task(t) for t in payload["tasks"]],
        actors={k: _actor(v) for k, v in payload["actors"].items()},
        task_progress={k: _progress(v) for k, v in payload.get("task_progress", {}).items()},
        cp_events={k: [_cp(e) for e in v] for k, v in payload.get("cp_events", {}).items()},
        task_results=dict(payload.get("task_results", {})),
        observed_commits=[_commit(c) for c in payload.get("observed_commits", [])],
        project_md=project_md,
        client_version=payload["client_version"],
        captured_at=payload["captured_at"],
    )


def _task(t: dict[str, Any]) -> TaskRecord:
    return TaskRecord(
        id=t["id"],
        title=t["title"],
        intent=t.get("intent"),
        acceptance=t.get("acceptance"),
        scope=list(t.get("scope") or []),
        depends_on=list(t.get("depends_on") or []),
        status=t["status"],
        assignee=t.get("assignee"),
        actor=t.get("actor"),
        claim_sha=t.get("claim_sha"),
        claim_at=t.get("claim_at"),
        done_at=t.get("done_at"),
        blocker=t.get("blocker"),
        parallel_lane=t.get("parallel_lane"),
        priority=t.get("priority"),
        capacity_hint=t.get("capacity_hint"),
    )


def _actor(a: dict[str, Any]) -> ActorRecord:
    return ActorRecord(
        display=a.get("display", ""),
        git_author_emails=list(a.get("git_author_emails") or []),
        git_author_names=list(a.get("git_author_names") or []),
        capacity=int(a.get("capacity", 1)),
    )


def _progress(p: dict[str, Any]) -> ProgressRecord:
    return ProgressRecord(
        done=int(p.get("done", 0)),
        total=int(p.get("total", 0)),
        current_cp=p.get("current_cp"),
        cp_names=list(p.get("cp_names") or []),
    )


def _cp(e: dict[str, Any]) -> CpEventRecord:
    return CpEventRecord(ts=e["ts"], actor=e["actor"], cp=e["cp"],
                         event=e["event"], note=e.get("note"))


def _commit(c: dict[str, Any]) -> CommitRecord:
    return CommitRecord(
        sha=c["sha"], author=c.get("author"), committed_at=c.get("committed_at"),
        subject=c.get("subject"), guessed_task_id=c.get("guessed_task_id"),
    )


def canonical_sha(payload: dict[str, Any]) -> str:
    body = {k: v for k, v in payload.items() if k not in {"snapshot_sha", "captured_at"}}
    serialized = json.dumps(body, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()
```

- [ ] **Step 5: Run, expect pass**

```bash
uv run pytest tests/test_parsers_wily_state.py -v
```
Expected: 4 passed.

- [ ] **Step 6: Commit**

```bash
git add app/parsers tests/contracts/agent_v1.json tests/test_parsers_wily_state.py
git commit -m "feat(parsers): agent_v1 payload validation"
```

---

## Task 6: Merge policy — last-write-wins for tasks

**Files:**
- Create: `wily-board/app/merge/__init__.py`
- Create: `wily-board/app/merge/policy.py`
- Create: `wily-board/tests/test_merge_policy_tasks.py`

- [ ] **Step 1: Write failing merge test**

Create `wily-board/tests/test_merge_policy_tasks.py`:
```python
import json
from pathlib import Path

from app.merge.policy import apply_snapshot
from app.parsers.wily_state import parse_snapshot

FIXTURE = Path(__file__).parent / "contracts" / "agent_v1.json"


def _seed(conn):
    conn.execute(
        "INSERT INTO projects(id, remote_url, title, mode_hint, first_seen_at, last_update_at)"
        " VALUES (?, ?, ?, ?, ?, ?)",
        ("9c1c1f0e7e9f6e3b7a1c4d4f7b8b9d2e8a3c2d1f", "git@x:y.git", "demo", "solo",
         "2026-01-01T00:00:00Z", "2026-01-01T00:00:00Z"),
    )
    conn.commit()


def test_apply_snapshot_inserts_task(conn):
    _seed(conn)
    parsed = parse_snapshot(json.loads(FIXTURE.read_text()))
    apply_snapshot(conn, parsed, machine_id="m1", received_at="2026-05-19T00:00:00Z")
    row = conn.execute(
        "SELECT title, parallel_lane, priority, capacity_hint, last_updated_by_machine "
        "FROM tasks WHERE project_id=? AND task_id='T04'",
        (parsed.project_id,),
    ).fetchone()
    assert row["title"] == "병렬 watch"
    assert row["parallel_lane"] == "ui"
    assert row["priority"] == 1
    assert row["capacity_hint"] == 2
    assert row["last_updated_by_machine"] == "m1"


def test_last_write_wins_on_status_flip(conn):
    _seed(conn)
    payload = json.loads(FIXTURE.read_text())
    parsed_old = parse_snapshot({**payload, "captured_at": "2026-05-19T00:00:00Z"})
    apply_snapshot(conn, parsed_old, machine_id="m1", received_at="2026-05-19T00:00:00Z")

    payload2 = json.loads(FIXTURE.read_text())
    payload2["tasks"][0]["status"] = "ready"
    parsed_new = parse_snapshot({**payload2, "captured_at": "2026-05-19T01:00:00Z"})
    apply_snapshot(conn, parsed_new, machine_id="m2", received_at="2026-05-19T01:00:00Z")

    row = conn.execute(
        "SELECT status, last_updated_by_machine FROM tasks "
        "WHERE project_id=? AND task_id='T04'",
        (parsed_new.project_id,),
    ).fetchone()
    assert row["status"] == "ready"
    assert row["last_updated_by_machine"] == "m2"


def test_task_progress_updated(conn):
    _seed(conn)
    parsed = parse_snapshot(json.loads(FIXTURE.read_text()))
    apply_snapshot(conn, parsed, machine_id="m1", received_at="2026-05-19T00:00:00Z")
    row = conn.execute(
        "SELECT cp_done, cp_total, cp_names_json FROM task_progress "
        "WHERE project_id=? AND task_id='T04'",
        (parsed.project_id,),
    ).fetchone()
    assert row["cp_done"] == 5
    assert row["cp_total"] == 5
```

- [ ] **Step 2: Run, expect fail**

```bash
uv run pytest tests/test_merge_policy_tasks.py -v
```
Expected: ImportError.

- [ ] **Step 3: Implement merge policy**

Create `wily-board/app/merge/__init__.py` (empty) and `wily-board/app/merge/policy.py`:
```python
from __future__ import annotations

import json
from sqlite3 import Connection

from app.parsers.wily_state import Snapshot


def apply_snapshot(conn: Connection, snap: Snapshot, *, machine_id: str,
                   received_at: str) -> None:
    _upsert_tasks(conn, snap, machine_id, received_at)
    _upsert_task_progress(conn, snap, received_at)
    _upsert_actors(conn, snap)
    _upsert_task_results(conn, snap, received_at)
    _insert_cp_events(conn, snap, machine_id)
    _insert_observed_commits(conn, snap)
    conn.commit()


def _upsert_tasks(conn, snap, machine_id, received_at):
    for t in snap.tasks:
        conn.execute(
            """INSERT INTO tasks(project_id, task_id, title, intent, acceptance,
                  scope_json, depends_on_json, status, assignee, actor,
                  claim_sha, claim_at, done_at, blocker,
                  parallel_lane, priority, capacity_hint,
                  last_updated_by_machine, last_updated_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(project_id, task_id) DO UPDATE SET
                 title=excluded.title, intent=excluded.intent,
                 acceptance=excluded.acceptance, scope_json=excluded.scope_json,
                 depends_on_json=excluded.depends_on_json, status=excluded.status,
                 assignee=excluded.assignee, actor=excluded.actor,
                 claim_sha=excluded.claim_sha, claim_at=excluded.claim_at,
                 done_at=excluded.done_at, blocker=excluded.blocker,
                 parallel_lane=excluded.parallel_lane, priority=excluded.priority,
                 capacity_hint=excluded.capacity_hint,
                 last_updated_by_machine=excluded.last_updated_by_machine,
                 last_updated_at=excluded.last_updated_at""",
            (snap.project_id, t.id, t.title, t.intent, t.acceptance,
             json.dumps(t.scope, ensure_ascii=False),
             json.dumps(t.depends_on, ensure_ascii=False),
             t.status, t.assignee, t.actor, t.claim_sha, t.claim_at,
             t.done_at, t.blocker, t.parallel_lane, t.priority, t.capacity_hint,
             machine_id, received_at),
        )


def _upsert_task_progress(conn, snap, received_at):
    for task_id, p in snap.task_progress.items():
        conn.execute(
            """INSERT INTO task_progress(project_id, task_id, cp_done, cp_total,
                 current_cp, cp_names_json, updated_at)
               VALUES (?,?,?,?,?,?,?)
               ON CONFLICT(project_id, task_id) DO UPDATE SET
                 cp_done=excluded.cp_done, cp_total=excluded.cp_total,
                 current_cp=excluded.current_cp, cp_names_json=excluded.cp_names_json,
                 updated_at=excluded.updated_at""",
            (snap.project_id, task_id, p.done, p.total, p.current_cp,
             json.dumps(p.cp_names, ensure_ascii=False), received_at),
        )


def _upsert_actors(conn, snap):
    for actor_id, a in snap.actors.items():
        conn.execute(
            """INSERT INTO project_actors(project_id, actor_id, display, capacity,
                 git_emails_json, git_names_json)
               VALUES (?,?,?,?,?,?)
               ON CONFLICT(project_id, actor_id) DO UPDATE SET
                 display=excluded.display, capacity=excluded.capacity,
                 git_emails_json=excluded.git_emails_json,
                 git_names_json=excluded.git_names_json""",
            (snap.project_id, actor_id, a.display, a.capacity,
             json.dumps(a.git_author_emails, ensure_ascii=False),
             json.dumps(a.git_author_names, ensure_ascii=False)),
        )


def _upsert_task_results(conn, snap, received_at):
    for task_id, body in snap.task_results.items():
        conn.execute(
            """INSERT INTO task_results(project_id, task_id, body, updated_at)
               VALUES (?,?,?,?)
               ON CONFLICT(project_id, task_id) DO UPDATE SET
                 body=excluded.body, updated_at=excluded.updated_at""",
            (snap.project_id, task_id, body, received_at),
        )


def _insert_cp_events(conn, snap, machine_id):
    for task_id, events in snap.cp_events.items():
        for e in events:
            conn.execute(
                """INSERT OR IGNORE INTO cp_events(project_id, task_id, ts, actor,
                     cp, event, note, ingest_machine)
                   VALUES (?,?,?,?,?,?,?,?)""",
                (snap.project_id, task_id, e.ts, e.actor, e.cp, e.event,
                 e.note, machine_id),
            )


def _insert_observed_commits(conn, snap):
    for c in snap.observed_commits:
        conn.execute(
            """INSERT OR IGNORE INTO observed_commits(project_id, sha, author,
                 committed_at, subject, guessed_task_id)
               VALUES (?,?,?,?,?,?)""",
            (snap.project_id, c.sha, c.author, c.committed_at, c.subject,
             c.guessed_task_id),
        )
```

- [ ] **Step 4: Run, expect pass**

```bash
uv run pytest tests/test_merge_policy_tasks.py -v
```
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add app/merge tests/test_merge_policy_tasks.py
git commit -m "feat(merge): apply_snapshot with last-write-wins"
```

---

## Task 7: Merge policy — append-only idempotency

**Files:**
- Create: `wily-board/tests/test_merge_policy_append.py`

- [ ] **Step 1: Write idempotency test**

Create `wily-board/tests/test_merge_policy_append.py`:
```python
import json
from pathlib import Path

from app.merge.policy import apply_snapshot
from app.parsers.wily_state import parse_snapshot

FIXTURE = Path(__file__).parent / "contracts" / "agent_v1.json"


def _seed(conn):
    conn.execute(
        "INSERT INTO projects(id, remote_url, title, mode_hint, first_seen_at, last_update_at)"
        " VALUES (?, ?, ?, ?, ?, ?)",
        ("9c1c1f0e7e9f6e3b7a1c4d4f7b8b9d2e8a3c2d1f", "git@x:y.git", "demo", "solo",
         "2026-01-01T00:00:00Z", "2026-01-01T00:00:00Z"),
    )
    conn.commit()


def test_cp_events_idempotent(conn):
    _seed(conn)
    parsed = parse_snapshot(json.loads(FIXTURE.read_text()))
    apply_snapshot(conn, parsed, machine_id="m1", received_at="2026-05-19T00:00:00Z")
    apply_snapshot(conn, parsed, machine_id="m1", received_at="2026-05-19T00:00:00Z")
    count = conn.execute(
        "SELECT COUNT(*) c FROM cp_events WHERE project_id=? AND task_id='T04'",
        (parsed.project_id,),
    ).fetchone()["c"]
    assert count == 2  # exactly the 2 events in fixture, not 4


def test_observed_commits_idempotent(conn):
    _seed(conn)
    parsed = parse_snapshot(json.loads(FIXTURE.read_text()))
    apply_snapshot(conn, parsed, machine_id="m1", received_at="2026-05-19T00:00:00Z")
    apply_snapshot(conn, parsed, machine_id="m2", received_at="2026-05-19T01:00:00Z")
    count = conn.execute(
        "SELECT COUNT(*) c FROM observed_commits WHERE project_id=? AND sha='296db49'",
        (parsed.project_id,),
    ).fetchone()["c"]
    assert count == 1
```

- [ ] **Step 2: Run, expect pass**

```bash
uv run pytest tests/test_merge_policy_append.py -v
```
Expected: 2 passed (the `INSERT OR IGNORE` from Task 6 already covers this).

- [ ] **Step 3: Commit**

```bash
git add tests/test_merge_policy_append.py
git commit -m "test(merge): append-only idempotency for cp/commits"
```

---

## Task 8: Session middleware

**Files:**
- Create: `wily-board/app/auth/__init__.py`
- Create: `wily-board/app/auth/sessions.py`
- Create: `wily-board/tests/test_auth_sessions.py`

- [ ] **Step 1: Write failing test**

Create `wily-board/tests/test_auth_sessions.py`:
```python
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.auth.sessions import SessionConfig, attach_sessions


def _app() -> FastAPI:
    app = FastAPI()
    attach_sessions(app, SessionConfig(secret="x" * 32, cookie_name="wb_s",
                                        max_age_seconds=3600))

    @app.post("/login")
    def login(request: Request):
        request.session["user_id"] = 42
        return {"ok": True}

    @app.get("/me")
    def me(request: Request):
        return {"user_id": request.session.get("user_id")}

    return app


def test_session_round_trip():
    client = TestClient(_app())
    r1 = client.post("/login")
    assert r1.status_code == 200
    cookie = r1.cookies.get("wb_s")
    assert cookie

    r2 = client.get("/me", cookies={"wb_s": cookie})
    assert r2.json() == {"user_id": 42}


def test_session_tamper_rejected():
    client = TestClient(_app())
    r = client.get("/me", cookies={"wb_s": "tampered"})
    assert r.json() == {"user_id": None}
```

- [ ] **Step 2: Run, expect fail**

```bash
uv run pytest tests/test_auth_sessions.py -v
```
Expected: ImportError.

- [ ] **Step 3: Implement**

Create `wily-board/app/auth/__init__.py` (empty) and `wily-board/app/auth/sessions.py`:
```python
from dataclasses import dataclass

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware


@dataclass
class SessionConfig:
    secret: str
    cookie_name: str
    max_age_seconds: int


def attach_sessions(app: FastAPI, cfg: SessionConfig) -> None:
    app.add_middleware(
        SessionMiddleware,
        secret_key=cfg.secret,
        session_cookie=cfg.cookie_name,
        max_age=cfg.max_age_seconds,
        same_site="lax",
        https_only=False,  # Caddy in front; behind proxy True via env override later
    )
```

- [ ] **Step 4: Run, expect pass**

```bash
uv run pytest tests/test_auth_sessions.py -v
```
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add app/auth/__init__.py app/auth/sessions.py tests/test_auth_sessions.py
git commit -m "feat(auth): signed cookie session middleware"
```

---

## Task 9: GitHub OAuth (mockable)

**Files:**
- Create: `wily-board/app/auth/github_oauth.py`
- Create: `wily-board/tests/test_auth_github_oauth.py`

- [ ] **Step 1: Write failing OAuth test**

Create `wily-board/tests/test_auth_github_oauth.py`:
```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.auth.github_oauth import GitHubOAuth, OAuthConfig, attach_oauth_routes
from app.auth.sessions import SessionConfig, attach_sessions


class FakeTransport:
    """Stub httpx transport that maps requests to canned responses."""
    def __init__(self):
        self.routes = {}

    def add(self, method, url, status, json_body):
        self.routes[(method, url)] = (status, json_body)

    def handle(self, request):
        import httpx
        key = (request.method, str(request.url))
        status, body = self.routes[key]
        return httpx.Response(status, json=body)


def _app(transport):
    app = FastAPI()
    attach_sessions(app, SessionConfig(secret="x" * 32, cookie_name="wb_s",
                                        max_age_seconds=3600))
    cfg = OAuthConfig(client_id="ci", client_secret="cs", redirect_uri="http://t/cb")
    oauth = GitHubOAuth(cfg, transport=transport)
    attach_oauth_routes(app, oauth)
    return app


def test_start_redirects_to_github():
    import httpx
    transport = httpx.MockTransport(FakeTransport().handle)  # noqa
    app = _app(transport)
    client = TestClient(app, follow_redirects=False)
    r = client.get("/auth/github/start")
    assert r.status_code == 302
    assert "github.com/login/oauth/authorize" in r.headers["location"]
    assert "state=" in r.headers["location"]


def test_callback_exchanges_code_and_sets_session():
    import httpx
    ft = FakeTransport()
    ft.add("POST", "https://github.com/login/oauth/access_token",
           200, {"access_token": "tok"})
    ft.add("GET", "https://api.github.com/user",
           200, {"id": 7, "login": "wily", "name": "Wily 박사", "avatar_url": "x"})
    transport = httpx.MockTransport(ft.handle)
    app = _app(transport)
    client = TestClient(app, follow_redirects=False)
    start = client.get("/auth/github/start")
    state = start.headers["location"].split("state=")[1].split("&")[0]

    r = client.get("/auth/github/callback", params={"code": "abc", "state": state})
    assert r.status_code == 302
    assert r.headers["location"].endswith("/")
    cookie = r.cookies.get("wb_s")
    assert cookie
```

- [ ] **Step 2: Run, expect fail**

```bash
uv run pytest tests/test_auth_github_oauth.py -v
```
Expected: ImportError.

- [ ] **Step 3: Implement OAuth**

Create `wily-board/app/auth/github_oauth.py`:
```python
from __future__ import annotations

import secrets
from dataclasses import dataclass
from typing import Any

import httpx
from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse

GITHUB_AUTHORIZE = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN = "https://github.com/login/oauth/access_token"
GITHUB_USER = "https://api.github.com/user"


@dataclass
class OAuthConfig:
    client_id: str
    client_secret: str
    redirect_uri: str


@dataclass
class GitHubUser:
    id: int
    login: str
    name: str | None
    avatar_url: str | None


class GitHubOAuth:
    def __init__(self, cfg: OAuthConfig,
                 transport: httpx.BaseTransport | None = None) -> None:
        self.cfg = cfg
        self._client = httpx.Client(transport=transport)

    def authorize_url(self, state: str) -> str:
        params = {
            "client_id": self.cfg.client_id,
            "redirect_uri": self.cfg.redirect_uri,
            "scope": "read:org read:user",
            "state": state,
        }
        return f"{GITHUB_AUTHORIZE}?{httpx.QueryParams(params)}"

    def exchange(self, code: str) -> str:
        r = self._client.post(
            GITHUB_TOKEN,
            data={
                "client_id": self.cfg.client_id,
                "client_secret": self.cfg.client_secret,
                "code": code,
                "redirect_uri": self.cfg.redirect_uri,
            },
            headers={"Accept": "application/json"},
        )
        r.raise_for_status()
        token = r.json().get("access_token")
        if not token:
            raise HTTPException(status_code=400, detail="no access_token from github")
        return token

    def user(self, access_token: str) -> GitHubUser:
        r = self._client.get(
            GITHUB_USER, headers={"Authorization": f"Bearer {access_token}"}
        )
        r.raise_for_status()
        data: Any = r.json()
        return GitHubUser(
            id=int(data["id"]), login=data["login"],
            name=data.get("name"), avatar_url=data.get("avatar_url"),
        )


def attach_oauth_routes(app: FastAPI, oauth: GitHubOAuth) -> None:
    router = APIRouter(prefix="/auth/github")

    @router.get("/start")
    def start(request: Request):
        state = secrets.token_urlsafe(16)
        request.session["oauth_state"] = state
        return RedirectResponse(oauth.authorize_url(state), status_code=302)

    @router.get("/callback")
    def callback(request: Request, code: str, state: str):
        if request.session.get("oauth_state") != state:
            raise HTTPException(status_code=400, detail="state mismatch")
        access_token = oauth.exchange(code)
        user = oauth.user(access_token)
        request.session["user_id"] = user.id
        request.session["user_login"] = user.login
        return RedirectResponse("/", status_code=302)

    app.include_router(router)
```

- [ ] **Step 4: Run, expect pass**

```bash
uv run pytest tests/test_auth_github_oauth.py -v
```
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add app/auth/github_oauth.py tests/test_auth_github_oauth.py
git commit -m "feat(auth): github oauth start/callback"
```

---

## Task 10: Org allowlist

**Files:**
- Create: `wily-board/app/auth/allowlist.py`
- Create: `wily-board/tests/test_auth_allowlist.py`

- [ ] **Step 1: Write failing test**

Create `wily-board/tests/test_auth_allowlist.py`:
```python
import httpx
import pytest

from app.auth.allowlist import AllowlistError, OrgAllowlist


def make_client(status: int) -> httpx.Client:
    def handler(request):
        return httpx.Response(status)
    return httpx.Client(transport=httpx.MockTransport(handler))


def test_member_passes():
    al = OrgAllowlist(org="R-W-LAB", admin_token="tok",
                      client=make_client(204))
    al.assert_member("wily")  # no exception


def test_non_member_rejected():
    al = OrgAllowlist(org="R-W-LAB", admin_token="tok",
                      client=make_client(404))
    with pytest.raises(AllowlistError):
        al.assert_member("attacker")
```

- [ ] **Step 2: Run, expect fail**

```bash
uv run pytest tests/test_auth_allowlist.py -v
```
Expected: ImportError.

- [ ] **Step 3: Implement**

Create `wily-board/app/auth/allowlist.py`:
```python
from dataclasses import dataclass

import httpx


class AllowlistError(Exception):
    pass


@dataclass
class OrgAllowlist:
    org: str
    admin_token: str
    client: httpx.Client

    def assert_member(self, login: str) -> None:
        url = f"https://api.github.com/orgs/{self.org}/members/{login}"
        r = self.client.get(url, headers={"Authorization": f"Bearer {self.admin_token}"})
        if r.status_code == 204:
            return
        raise AllowlistError(f"{login} is not a member of {self.org}")
```

- [ ] **Step 4: Run, expect pass**

```bash
uv run pytest tests/test_auth_allowlist.py -v
```
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add app/auth/allowlist.py tests/test_auth_allowlist.py
git commit -m "feat(auth): R-W-LAB org allowlist"
```

---

## Task 11: One-time code minting via `/web/machines`

**Files:**
- Create: `wily-board/app/api/__init__.py`
- Create: `wily-board/app/api/machines.py`
- Create: `wily-board/tests/test_api_machines.py`

- [ ] **Step 1: Write failing test**

Create `wily-board/tests/test_api_machines.py`:
```python
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.api.machines import attach_machine_routes
from app.auth.sessions import SessionConfig, attach_sessions
from app.db import repo


def _app(conn, *, login_as: int | None = None):
    app = FastAPI()
    attach_sessions(app, SessionConfig(secret="x" * 32, cookie_name="wb_s",
                                        max_age_seconds=3600))
    attach_machine_routes(app, lambda: conn)

    @app.post("/_test/login")
    def _login(request: Request):
        if login_as is not None:
            request.session["user_id"] = login_as
        return {"ok": True}

    return app


def test_mint_requires_login(conn):
    client = TestClient(_app(conn))
    r = client.post("/web/machines", json={"hostname": "laptop"})
    assert r.status_code == 401


def test_mint_returns_one_time_code(conn):
    repo.upsert_user(conn, github_id=1, login="wily", display="", avatar_url="",
                     role="wily", created_at="2026-05-19T00:00:00Z")
    client = TestClient(_app(conn, login_as=1))
    client.post("/_test/login")  # establish session

    r = client.post("/web/machines", json={"hostname": "laptop"})
    assert r.status_code == 200, r.text
    body = r.json()
    assert "code" in body and len(body["code"]) >= 12
    assert "expires_at" in body
```

- [ ] **Step 2: Run, expect fail**

```bash
uv run pytest tests/test_api_machines.py -v
```
Expected: ImportError.

- [ ] **Step 3: Implement `app/api/machines.py`**

Create `wily-board/app/api/__init__.py` (empty) and `wily-board/app/api/machines.py`:
```python
from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone
from sqlite3 import Connection
from typing import Callable

from fastapi import APIRouter, FastAPI, HTTPException, Request
from pydantic import BaseModel

CODE_TTL_SECONDS = 600

_codes: dict[str, dict] = {}  # in-memory; survives single-process server


class MintRequest(BaseModel):
    hostname: str


def attach_machine_routes(app: FastAPI, conn_provider: Callable[[], Connection]) -> None:
    router = APIRouter(prefix="/web")

    @router.post("/machines")
    def mint(request: Request, body: MintRequest):
        user_id = request.session.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="login required")
        code = secrets.token_urlsafe(12)
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=CODE_TTL_SECONDS)
        _codes[code] = {
            "user_id": user_id, "hostname": body.hostname,
            "expires_at": expires_at,
        }
        return {"code": code, "expires_at": expires_at.isoformat()}

    app.include_router(router)


def consume_code(code: str) -> dict | None:
    entry = _codes.pop(code, None)
    if not entry:
        return None
    if entry["expires_at"] < datetime.now(timezone.utc):
        return None
    return entry
```

- [ ] **Step 4: Run, expect pass**

```bash
uv run pytest tests/test_api_machines.py -v
```
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add app/api/__init__.py app/api/machines.py tests/test_api_machines.py
git commit -m "feat(api): one-time code mint for machine registration"
```

---

## Task 12: `/agent/register` exchange

**Files:**
- Create: `wily-board/app/api/agent.py`
- Create: `wily-board/tests/test_api_agent_register.py`

- [ ] **Step 1: Write failing test**

Create `wily-board/tests/test_api_agent_register.py`:
```python
import hashlib

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.agent import attach_agent_routes
from app.api.machines import _codes
from datetime import datetime, timedelta, timezone

from app.db import repo


def _app(conn):
    app = FastAPI()
    attach_agent_routes(app, lambda: conn, pepper="pep")
    return app


def test_register_with_valid_code_returns_token(conn):
    repo.upsert_user(conn, github_id=1, login="wily", display="", avatar_url="",
                     role="wily", created_at="2026-05-19T00:00:00Z")
    _codes["abc"] = {"user_id": 1, "hostname": "laptop",
                     "expires_at": datetime.now(timezone.utc) + timedelta(minutes=5)}
    app = _app(conn)
    r = TestClient(app).post("/agent/register", json={"code": "abc"})
    assert r.status_code == 200
    body = r.json()
    assert body["machine_id"]
    assert body["token"]
    h = hashlib.sha256(("pep" + body["token"]).encode()).hexdigest()
    assert conn.execute(
        "SELECT 1 FROM machines WHERE token_hash=?", (h,)
    ).fetchone() is not None


def test_register_rejects_invalid_code(conn):
    app = _app(conn)
    r = TestClient(app).post("/agent/register", json={"code": "nope"})
    assert r.status_code == 400
```

- [ ] **Step 2: Run, expect fail**

```bash
uv run pytest tests/test_api_agent_register.py -v
```
Expected: ImportError.

- [ ] **Step 3: Implement `/agent/register`**

Create `wily-board/app/api/agent.py`:
```python
from __future__ import annotations

import hashlib
import secrets
import uuid
from datetime import datetime, timezone
from sqlite3 import Connection
from typing import Callable

from fastapi import APIRouter, FastAPI, Header, HTTPException
from pydantic import BaseModel

from app.api.machines import consume_code
from app.db import repo


class RegisterReq(BaseModel):
    code: str


def _hash_token(token: str, pepper: str) -> str:
    return hashlib.sha256((pepper + token).encode("utf-8")).hexdigest()


def attach_agent_routes(app: FastAPI, conn_provider: Callable[[], Connection],
                        *, pepper: str) -> None:
    router = APIRouter(prefix="/agent")

    @router.post("/register")
    def register(body: RegisterReq):
        entry = consume_code(body.code)
        if not entry:
            raise HTTPException(status_code=400, detail="invalid or expired code")
        token = secrets.token_urlsafe(32)
        machine_id = str(uuid.uuid4())
        repo.create_machine(
            conn_provider(),
            machine_id=machine_id,
            user_id=entry["user_id"],
            hostname=entry["hostname"],
            token_hash=_hash_token(token, pepper),
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        return {"machine_id": machine_id, "token": token}

    app.include_router(router)


def auth_machine(conn: Connection, pepper: str, header: str | None) -> dict:
    if not header or not header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing bearer")
    token = header.removeprefix("Bearer ").strip()
    machine = repo.find_machine_by_token_hash(conn, _hash_token(token, pepper))
    if not machine:
        raise HTTPException(status_code=401, detail="invalid token")
    return machine
```

- [ ] **Step 4: Run, expect pass**

```bash
uv run pytest tests/test_api_agent_register.py -v
```
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add app/api/agent.py tests/test_api_agent_register.py
git commit -m "feat(api): agent token registration"
```

---

## Task 13: `/agent/snapshot` ingest

**Files:**
- Modify: `wily-board/app/api/agent.py` (add /snapshot endpoint)
- Create: `wily-board/tests/test_api_agent_snapshot.py`

- [ ] **Step 1: Write failing test**

Create `wily-board/tests/test_api_agent_snapshot.py`:
```python
import json
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.agent import attach_agent_routes
from app.db import repo

FIXTURE = Path(__file__).parent / "contracts" / "agent_v1.json"


def _seed_machine_with_token(conn, *, pepper="pep", token="TOK") -> None:
    import hashlib
    repo.upsert_user(conn, github_id=1, login="wily", display="", avatar_url="",
                     role="wily", created_at="2026-05-19T00:00:00Z")
    repo.create_machine(
        conn, machine_id="m1", user_id=1, hostname="laptop",
        token_hash=hashlib.sha256((pepper + token).encode()).hexdigest(),
        created_at=datetime.now(timezone.utc).isoformat(),
    )


def _client(conn, pepper="pep"):
    app = FastAPI()
    attach_agent_routes(app, lambda: conn, pepper=pepper)
    return TestClient(app)


def test_snapshot_inserts_tasks_and_events(conn):
    _seed_machine_with_token(conn)

    payload = json.loads(FIXTURE.read_text())
    r = _client(conn).post("/agent/snapshot", json=payload,
                           headers={"Authorization": "Bearer TOK"})
    assert r.status_code == 200, r.text
    pid = payload["project_id"]

    row = conn.execute("SELECT title FROM tasks WHERE project_id=? AND task_id='T04'",
                       (pid,)).fetchone()
    assert row["title"] == "병렬 watch"

    ev = conn.execute(
        "SELECT type FROM agent_events WHERE machine_id='m1' ORDER BY id DESC LIMIT 1"
    ).fetchone()
    assert ev["type"] == "snapshot"


def test_snapshot_requires_auth(conn):
    payload = json.loads(FIXTURE.read_text())
    r = _client(conn).post("/agent/snapshot", json=payload)
    assert r.status_code == 401


def test_snapshot_noop_on_same_sha(conn):
    _seed_machine_with_token(conn)
    payload = json.loads(FIXTURE.read_text())
    payload["snapshot_sha"] = "fixed-sha-value"

    client = _client(conn)
    r1 = client.post("/agent/snapshot", json=payload,
                     headers={"Authorization": "Bearer TOK"})
    assert r1.status_code == 200
    r2 = client.post("/agent/snapshot", json=payload,
                     headers={"Authorization": "Bearer TOK"})
    assert r2.json()["noop"] is True
```

- [ ] **Step 2: Run, expect fail**

```bash
uv run pytest tests/test_api_agent_snapshot.py -v
```
Expected: ImportError / route not found.

- [ ] **Step 3: Add `/agent/snapshot` to `app/api/agent.py`**

Append to `wily-board/app/api/agent.py` (extend the router inside `attach_agent_routes`):
```python
    from typing import Any

    from app.merge.policy import apply_snapshot
    from app.parsers.wily_state import ParseError, parse_snapshot

    @router.post("/snapshot")
    def snapshot(payload: dict[str, Any],
                 authorization: str | None = Header(default=None)):
        conn = conn_provider()
        machine = auth_machine(conn, pepper, authorization)
        try:
            parsed = parse_snapshot(payload)
        except ParseError as e:
            raise HTTPException(status_code=400, detail=str(e))

        # idempotency: check last snapshot_sha for this (project, machine)
        prev = conn.execute(
            "SELECT snapshot_sha FROM task_snapshots WHERE project_id=? AND machine_id=?",
            (parsed.project_id, machine["id"]),
        ).fetchone()
        if prev and prev["snapshot_sha"] == parsed.snapshot_sha:
            return {"noop": True}

        now = datetime.now(timezone.utc).isoformat()
        # ensure project row exists
        existing = conn.execute(
            "SELECT 1 FROM projects WHERE id=?", (parsed.project_id,)
        ).fetchone()
        first_seen = now if not existing else None
        repo.upsert_project(
            conn, project_id=parsed.project_id, remote_url=parsed.remote_url,
            title=parsed.title, mode_hint=parsed.mode_hint,
            first_seen_at=first_seen or now, last_update_at=now,
        )
        conn.execute(
            """INSERT INTO task_snapshots(project_id, machine_id, snapshot_sha,
                 tasks_json, project_md, actors_json, updated_at)
               VALUES (?,?,?,?,?,?,?)
               ON CONFLICT(project_id, machine_id) DO UPDATE SET
                 snapshot_sha=excluded.snapshot_sha,
                 tasks_json=excluded.tasks_json,
                 project_md=excluded.project_md,
                 actors_json=excluded.actors_json,
                 updated_at=excluded.updated_at""",
            (parsed.project_id, machine["id"], parsed.snapshot_sha,
             json.dumps([t.__dict__ for t in parsed.tasks], ensure_ascii=False),
             parsed.project_md,
             json.dumps({k: v.__dict__ for k, v in parsed.actors.items()},
                        ensure_ascii=False),
             now),
        )
        apply_snapshot(conn, parsed, machine_id=machine["id"], received_at=now)
        conn.execute(
            "INSERT INTO agent_events(machine_id, project_id, type, payload, created_at)"
            " VALUES (?,?,?,?,?)",
            (machine["id"], parsed.project_id, "snapshot",
             json.dumps({"snapshot_sha": parsed.snapshot_sha}), now),
        )
        conn.commit()
        return {"noop": False, "project_id": parsed.project_id}
```

Also add at top of file: `import json`.

- [ ] **Step 4: Run, expect pass**

```bash
uv run pytest tests/test_api_agent_snapshot.py -v
```
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add app/api/agent.py tests/test_api_agent_snapshot.py
git commit -m "feat(api): agent snapshot ingest with idempotency"
```

---

## Task 14: `/agent/heartbeat` and presence

**Files:**
- Modify: `wily-board/app/api/agent.py`
- Create: `wily-board/tests/test_api_agent_heartbeat.py`

- [ ] **Step 1: Write failing test**

Create `wily-board/tests/test_api_agent_heartbeat.py`:
```python
import hashlib
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.agent import attach_agent_routes
from app.db import repo


def _setup(conn):
    repo.upsert_user(conn, github_id=1, login="wily", display="", avatar_url="",
                     role="wily", created_at="2026-05-19T00:00:00Z")
    repo.create_machine(
        conn, machine_id="m1", user_id=1, hostname="laptop",
        token_hash=hashlib.sha256(("pep" + "TOK").encode()).hexdigest(),
        created_at=datetime.now(timezone.utc).isoformat(),
    )


def _client(conn):
    app = FastAPI()
    attach_agent_routes(app, lambda: conn, pepper="pep")
    return TestClient(app)


def test_heartbeat_upserts_presence(conn):
    _setup(conn)
    r = _client(conn).post(
        "/agent/heartbeat",
        json={"project_id": "p1", "current_task_id": "T04"},
        headers={"Authorization": "Bearer TOK"},
    )
    assert r.status_code == 200
    row = conn.execute(
        "SELECT current_project_id, current_task_id FROM actor_presence "
        "WHERE user_id=1 AND machine_id='m1'"
    ).fetchone()
    assert row["current_project_id"] == "p1"
    assert row["current_task_id"] == "T04"


def test_heartbeat_requires_auth(conn):
    _setup(conn)
    r = _client(conn).post("/agent/heartbeat", json={})
    assert r.status_code == 401
```

- [ ] **Step 2: Run, expect fail**

```bash
uv run pytest tests/test_api_agent_heartbeat.py -v
```
Expected: route not found.

- [ ] **Step 3: Add `/agent/heartbeat`**

Append to the router inside `attach_agent_routes` in `wily-board/app/api/agent.py`:
```python
    class HeartbeatReq(BaseModel):
        project_id: str | None = None
        current_task_id: str | None = None

    @router.post("/heartbeat")
    def heartbeat(body: HeartbeatReq,
                  authorization: str | None = Header(default=None)):
        conn = conn_provider()
        machine = auth_machine(conn, pepper, authorization)
        now = datetime.now(timezone.utc).isoformat()
        conn.execute(
            """INSERT INTO actor_presence(user_id, machine_id,
                 current_project_id, current_task_id, last_seen)
               VALUES (?,?,?,?,?)
               ON CONFLICT(user_id, machine_id) DO UPDATE SET
                 current_project_id=excluded.current_project_id,
                 current_task_id=excluded.current_task_id,
                 last_seen=excluded.last_seen""",
            (machine["user_id"], machine["id"],
             body.project_id, body.current_task_id, now),
        )
        conn.execute(
            "UPDATE machines SET last_seen=? WHERE id=?", (now, machine["id"])
        )
        conn.commit()
        return {"ok": True}
```

Add `from pydantic import BaseModel` at top if not already imported.

- [ ] **Step 4: Run, expect pass**

```bash
uv run pytest tests/test_api_agent_heartbeat.py -v
```
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add app/api/agent.py tests/test_api_agent_heartbeat.py
git commit -m "feat(api): agent heartbeat updates presence"
```

---

## Task 15: Web shell — base templates and login flow

**Files:**
- Create: `wily-board/app/web/__init__.py`
- Create: `wily-board/app/web/routes.py`
- Create: `wily-board/app/web/templates/base.html`
- Create: `wily-board/app/web/templates/login.html`
- Create: `wily-board/app/web/templates/machines.html`
- Create: `wily-board/app/web/static/pico.min.css` (vendored — download in step)
- Create: `wily-board/app/web/static/app.css`
- Create: `wily-board/tests/test_web_routes.py`

- [ ] **Step 1: Vendor Pico.css and create static skeleton**

```bash
mkdir -p app/web/static
curl -L https://unpkg.com/@picocss/pico@2/css/pico.min.css \
  -o app/web/static/pico.min.css
```

Create `wily-board/app/web/static/app.css`:
```css
:root {
  --wb-bg: #fafafa;
  --wb-surface: #ffffff;
  --wb-border: #e4e4e7;
  --wb-text: #18181b;
  --wb-text-muted: #71717a;
  --wb-accent: #5b8def;
}
@media (prefers-color-scheme: dark) {
  :root {
    --wb-bg: #0b0c0f;
    --wb-surface: #15171c;
    --wb-border: #2a2d36;
    --wb-text: #f4f4f5;
    --wb-text-muted: #a1a1aa;
    --wb-accent: #7aa7ff;
  }
}
body { background: var(--wb-bg); color: var(--wb-text); }
.shell-topbar { display: flex; align-items: center; gap: 12px;
                padding: 12px 16px; border-bottom: 1px solid var(--wb-border); }
```

- [ ] **Step 2: Write templates**

Create `wily-board/app/web/templates/base.html`:
```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}Wily Board{% endblock %}</title>
  <link rel="stylesheet" href="/static/pico.min.css">
  <link rel="stylesheet" href="/static/app.css">
</head>
<body>
  <header class="shell-topbar">
    <strong>Wily Board</strong>
    <div style="margin-left:auto">
      {% if user_login %}{{ user_login }} · <a href="/auth/logout">로그아웃</a>{% endif %}
    </div>
  </header>
  <main class="container">{% block content %}{% endblock %}</main>
</body>
</html>
```

Create `wily-board/app/web/templates/login.html`:
```html
{% extends "base.html" %}
{% block content %}
  <h2>로그인이 필요합니다</h2>
  <p><a href="/auth/github/start" role="button">GitHub로 로그인</a></p>
{% endblock %}
```

Create `wily-board/app/web/templates/machines.html`:
```html
{% extends "base.html" %}
{% block content %}
  <h2>머신 등록</h2>
  <p>로컬에서 다음을 실행하세요:</p>
  <pre>wily-agent login {{ code }}</pre>
  <p><small>유효 만료: {{ expires_at }}</small></p>
{% endblock %}
```

- [ ] **Step 3: Write failing route test**

Create `wily-board/tests/test_web_routes.py`:
```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.auth.sessions import SessionConfig, attach_sessions
from app.web.routes import attach_web_routes


def _app():
    app = FastAPI()
    attach_sessions(app, SessionConfig(secret="x" * 32, cookie_name="wb_s",
                                        max_age_seconds=3600))
    attach_web_routes(app)
    return app


def test_root_redirects_when_unauthed():
    client = TestClient(_app(), follow_redirects=False)
    r = client.get("/")
    assert r.status_code in (302, 303)
    assert r.headers["location"].endswith("/login")


def test_login_page_renders():
    r = TestClient(_app()).get("/login")
    assert r.status_code == 200
    assert "GitHub로 로그인" in r.text
```

- [ ] **Step 4: Run, expect fail**

```bash
uv run pytest tests/test_web_routes.py -v
```
Expected: ImportError.

- [ ] **Step 5: Implement `app/web/routes.py`**

Create `wily-board/app/web/__init__.py` (empty) and `wily-board/app/web/routes.py`:
```python
from pathlib import Path

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

TEMPLATES = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


def attach_web_routes(app: FastAPI) -> None:
    static_dir = Path(__file__).parent / "static"
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    router = APIRouter()

    @router.get("/", response_class=HTMLResponse)
    def index(request: Request):
        if not request.session.get("user_id"):
            return RedirectResponse("/login", status_code=303)
        return TEMPLATES.TemplateResponse(
            "base.html",
            {"request": request, "user_login": request.session.get("user_login")},
        )

    @router.get("/login", response_class=HTMLResponse)
    def login(request: Request):
        return TEMPLATES.TemplateResponse(
            "login.html", {"request": request, "user_login": None}
        )

    app.include_router(router)
```

- [ ] **Step 6: Run, expect pass**

```bash
uv run pytest tests/test_web_routes.py -v
```
Expected: 2 passed.

- [ ] **Step 7: Commit**

```bash
git add app/web tests/test_web_routes.py
git commit -m "feat(web): minimal login shell + pico/jinja static"
```

---

## Task 16: Wire everything in `app/main.py`

**Files:**
- Create: `wily-board/app/main.py`
- Create: `wily-board/tests/test_main_app.py`

- [ ] **Step 1: Write failing integration test**

Create `wily-board/tests/test_main_app.py`:
```python
import os

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def app_env(tmp_path, monkeypatch):
    monkeypatch.setenv("WB_SESSION_SECRET", "x" * 32)
    monkeypatch.setenv("WB_GITHUB_CLIENT_ID", "ci")
    monkeypatch.setenv("WB_GITHUB_CLIENT_SECRET", "cs")
    monkeypatch.setenv("WB_GITHUB_ORG", "R-W-LAB")
    monkeypatch.setenv("WB_BASE_URL", "http://test/")
    monkeypatch.setenv("WB_SQLITE_PATH", str(tmp_path / "board.sqlite"))
    monkeypatch.setenv("WB_AGENT_TOKEN_PEPPER", "pep")
    yield


def test_app_boots_and_serves_login(app_env):
    from app.main import build_app
    client = TestClient(build_app())
    r = client.get("/login")
    assert r.status_code == 200
    assert "GitHub로 로그인" in r.text


def test_app_creates_sqlite_schema(app_env, tmp_path):
    from app.main import build_app
    build_app()
    import sqlite3
    db = tmp_path / "board.sqlite"
    assert db.exists()
    conn = sqlite3.connect(db)
    names = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    assert "tasks" in names and "cp_events" in names
```

- [ ] **Step 2: Run, expect fail**

```bash
uv run pytest tests/test_main_app.py -v
```
Expected: ImportError.

- [ ] **Step 3: Implement `app/main.py`**

Create `wily-board/app/main.py`:
```python
from __future__ import annotations

import sqlite3
from pathlib import Path

import httpx
from fastapi import FastAPI

from app.api.agent import attach_agent_routes
from app.api.machines import attach_machine_routes
from app.auth.github_oauth import GitHubOAuth, OAuthConfig, attach_oauth_routes
from app.auth.sessions import SessionConfig, attach_sessions
from app.config import Settings
from app.db.migrations import apply_schema
from app.web.routes import attach_web_routes


def _ensure_db(path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    apply_schema(conn)
    conn.close()


def _open(path: str) -> sqlite3.Connection:
    c = sqlite3.connect(path, check_same_thread=False)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys = ON")
    return c


def build_app() -> FastAPI:
    import os

    settings = Settings()
    _ensure_db(settings.sqlite_path)
    conn = _open(settings.sqlite_path)

    app = FastAPI(title="wily-board")
    attach_sessions(app, SessionConfig(
        secret=settings.session_secret,
        cookie_name=settings.session_cookie_name,
        max_age_seconds=settings.session_max_age_seconds,
    ))
    oauth = GitHubOAuth(
        OAuthConfig(
            client_id=settings.github_client_id,
            client_secret=settings.github_client_secret,
            redirect_uri=f"{settings.base_url.rstrip('/')}/auth/github/callback",
        ),
        transport=httpx.HTTPTransport(),
    )
    attach_oauth_routes(app, oauth)
    attach_machine_routes(app, lambda: conn)
    attach_agent_routes(app, lambda: conn, pepper=settings.agent_token_pepper)
    attach_web_routes(app)

    if os.environ.get("WB_DEBUG_TEST_LOGIN") == "1":
        from fastapi import Request

        @app.post("/_test/login")
        def _test_login(request: Request, user_id: int):
            request.session["user_id"] = user_id
            return {"ok": True}

    return app


app = build_app() if __name__ != "__main__" else None
```

- [ ] **Step 4: Run, expect pass**

```bash
uv run pytest tests/test_main_app.py -v
```
Expected: 2 passed.

- [ ] **Step 5: Full suite green check**

```bash
uv run pytest -v
```
Expected: all tests pass.

- [ ] **Step 6: Commit**

```bash
git add app/main.py tests/test_main_app.py
git commit -m "feat(app): main wiring + sqlite bootstrap"
```

---

## Task 17: Deployment artifacts

**Files:**
- Create: `wily-board/deploy/Caddyfile`
- Create: `wily-board/deploy/wily-board.service`
- Create: `wily-board/deploy/install.sh`
- Create: `wily-board/deploy/backup.sh`

- [ ] **Step 1: Write `Caddyfile`**

Create `wily-board/deploy/Caddyfile`:
```
{$WILY_BOARD_HOST} {
  encode gzip

  @auth path /auth/*
  rate_limit @auth 10r/m

  @agent path /agent/*
  rate_limit @agent 600r/m

  @web path /web/* /static/* /
  rate_limit @web 60r/m

  reverse_proxy 127.0.0.1:8080
}
```

- [ ] **Step 2: Write systemd unit**

Create `wily-board/deploy/wily-board.service`:
```ini
[Unit]
Description=Wily Board v3
After=network-online.target

[Service]
Type=simple
User=wily-board
WorkingDirectory=/opt/wily-board
EnvironmentFile=/etc/wily-board.env
ExecStart=/opt/wily-board/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8080 --workers 1
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

- [ ] **Step 3: Write `install.sh`**

Create `wily-board/deploy/install.sh` (mark executable in step 5):
```bash
#!/usr/bin/env bash
set -euo pipefail

INSTALL_DIR=/opt/wily-board
ENV_FILE=/etc/wily-board.env

sudo useradd --system --home "$INSTALL_DIR" --shell /usr/sbin/nologin wily-board || true
sudo mkdir -p "$INSTALL_DIR" /var/lib/wily-board
sudo chown -R wily-board:wily-board "$INSTALL_DIR" /var/lib/wily-board

sudo -u wily-board git clone https://github.com/R-W-LAB/wily-board "$INSTALL_DIR"
cd "$INSTALL_DIR"
sudo -u wily-board uv sync

if [ ! -f "$ENV_FILE" ]; then
  sudo tee "$ENV_FILE" >/dev/null <<EOF
WB_HOST=127.0.0.1
WB_PORT=8080
WB_SQLITE_PATH=/var/lib/wily-board/board.sqlite
WB_SESSION_SECRET=$(openssl rand -hex 32)
WB_AGENT_TOKEN_PEPPER=$(openssl rand -hex 16)
WB_GITHUB_CLIENT_ID=__SET_ME__
WB_GITHUB_CLIENT_SECRET=__SET_ME__
WB_GITHUB_ORG=R-W-LAB
WB_BASE_URL=https://__SET_ME__
EOF
  sudo chmod 600 "$ENV_FILE"
fi

sudo cp deploy/wily-board.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable wily-board

echo "Edit $ENV_FILE then: sudo systemctl start wily-board"
```

- [ ] **Step 4: Write `backup.sh`**

Create `wily-board/deploy/backup.sh`:
```bash
#!/usr/bin/env bash
set -euo pipefail

SRC=/var/lib/wily-board/board.sqlite
DST=/var/backups/wily-board
STAMP=$(date -u +%Y%m%d-%H%M%S)

sudo mkdir -p "$DST"
sudo sqlite3 "$SRC" ".backup '$DST/board-$STAMP.sqlite'"
sudo find "$DST" -name 'board-*.sqlite' -mtime +14 -delete
```

- [ ] **Step 5: Mark scripts executable + commit**

```bash
chmod +x deploy/install.sh deploy/backup.sh
git add deploy
git commit -m "feat(deploy): Caddyfile, systemd unit, install/backup scripts"
```

---

## Task 18: End-to-end smoke test

**Files:**
- Create: `wily-board/tests/test_smoke_end_to_end.py`

- [ ] **Step 1: Write smoke test**

Create `wily-board/tests/test_smoke_end_to_end.py`:
```python
import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi.testclient import TestClient

FIXTURE = Path(__file__).parent / "contracts" / "agent_v1.json"


def test_full_flow_mint_register_snapshot_heartbeat(tmp_path, monkeypatch):
    monkeypatch.setenv("WB_SESSION_SECRET", "x" * 32)
    monkeypatch.setenv("WB_GITHUB_CLIENT_ID", "ci")
    monkeypatch.setenv("WB_GITHUB_CLIENT_SECRET", "cs")
    monkeypatch.setenv("WB_GITHUB_ORG", "R-W-LAB")
    monkeypatch.setenv("WB_BASE_URL", "http://test/")
    monkeypatch.setenv("WB_SQLITE_PATH", str(tmp_path / "board.sqlite"))
    monkeypatch.setenv("WB_AGENT_TOKEN_PEPPER", "pep")
    monkeypatch.setenv("WB_DEBUG_TEST_LOGIN", "1")  # enables /_test/login route

    from app.main import build_app
    from app.db import repo
    import sqlite3

    app = build_app()
    client = TestClient(app)

    # Seed a user directly
    conn = sqlite3.connect(tmp_path / "board.sqlite")
    conn.row_factory = sqlite3.Row
    repo.upsert_user(conn, github_id=1, login="wily", display="", avatar_url="",
                     role="wily", created_at="2026-05-19T00:00:00Z")
    conn.commit()
    conn.close()

    # Establish a session via the debug login route (enabled by WB_DEBUG_TEST_LOGIN=1)
    login = client.post("/_test/login", params={"user_id": 1})
    assert login.status_code == 200

    # 1. Mint a one-time code
    mint = client.post("/web/machines", json={"hostname": "laptop"})
    assert mint.status_code == 200, mint.text
    code = mint.json()["code"]

    # 2. Exchange code for machine token
    reg = client.post("/agent/register", json={"code": code})
    assert reg.status_code == 200
    token = reg.json()["token"]

    # 3. POST snapshot
    payload = json.loads(FIXTURE.read_text())
    snap = client.post(
        "/agent/snapshot", json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert snap.status_code == 200, snap.text

    # 4. POST heartbeat
    hb = client.post(
        "/agent/heartbeat",
        json={"project_id": payload["project_id"], "current_task_id": "T04"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert hb.status_code == 200

    # 5. Verify DB rows
    conn = sqlite3.connect(tmp_path / "board.sqlite")
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT title FROM tasks WHERE project_id=? AND task_id='T04'",
        (payload["project_id"],),
    ).fetchone()
    assert row["title"] == "병렬 watch"
    presence = conn.execute(
        "SELECT current_task_id FROM actor_presence WHERE user_id=1"
    ).fetchone()
    assert presence["current_task_id"] == "T04"
    conn.close()
```

> The smoke test enables the debug-only `/_test/login` route by setting `WB_DEBUG_TEST_LOGIN=1` (defined in `app/main.py` Task 16). The OAuth path is already covered by Task 9's mocked tests; the smoke focuses on the data ingest path.

- [ ] **Step 2: Run, expect pass**

```bash
uv run pytest tests/test_smoke_end_to_end.py -v
```
Expected: 1 passed.

- [ ] **Step 3: Full suite + ruff + commit**

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest -v
```
Expected: ruff clean, all tests pass.

```bash
git add tests/test_smoke_end_to_end.py
git commit -m "test(smoke): mint -> register -> snapshot -> heartbeat round-trip"
```

---

## Task 19: README + migration runbook

**Files:**
- Modify: `wily-board/README.md`
- Create: `wily-board/docs/deploy.md`

- [ ] **Step 1: Rewrite README**

Replace `wily-board/README.md` with:
```markdown
# Wily Board

Read-only web board for Wily Roadmap v3. Visualises every wily v3 project on
your machines plus R-W-LAB shared projects, refreshed in real time by a local
sync agent. Design spec: `wily-roadmap/docs/superpowers/specs/2026-05-19-wily-board-v3-design.md`.

## Development

```bash
uv sync --extra dev
uv run pytest -v
uv run uvicorn app.main:app --reload
```

## Configuration

Required env vars (or `.env` file). Generated by `deploy/install.sh`:

| Variable | Description |
|---|---|
| `WB_SESSION_SECRET` | ≥ 32 random bytes (signed cookies) |
| `WB_AGENT_TOKEN_PEPPER` | random 16+ bytes (token hashing) |
| `WB_GITHUB_CLIENT_ID` | GitHub OAuth app id |
| `WB_GITHUB_CLIENT_SECRET` | GitHub OAuth app secret |
| `WB_GITHUB_ORG` | `R-W-LAB` (allowlist org) |
| `WB_BASE_URL` | public https URL |
| `WB_SQLITE_PATH` | DB file path (default `var/board.sqlite`) |

## Deployment

See `docs/deploy.md`.
```

- [ ] **Step 2: Write `docs/deploy.md`**

Create `wily-board/docs/deploy.md`:
```markdown
# Deployment runbook

## v2 → v3 migration

1. On the existing Azure VM, stop the v2 service: `sudo systemctl stop wily-board`.
2. Back up the v2 SQLite: `sudo cp /var/lib/wily-board/board.sqlite /var/backups/wily-board/board.v2.sqlite`.
3. On the repo side, push `legacy/v2` branch and force-push the new `main` from this plan's commits.
4. Re-run `deploy/install.sh` on the VM (it preserves `/etc/wily-board.env`).
5. `sudo systemctl daemon-reload && sudo systemctl restart wily-board`.
6. Verify health: `curl -fsS https://<host>/login | grep '로그인'`.
7. Add GitHub OAuth callback URL `https://<host>/auth/github/callback` in the OAuth app settings.
8. Log in as Wily; verify dashboard renders (empty until agents register).

## First-time verification

After install:

- [ ] `/login` returns 200 with the GitHub button.
- [ ] OAuth round-trip lands on `/` and sets cookie.
- [ ] `POST /agent/register` with an unknown code returns 400.
- [ ] After minting a code via `POST /web/machines`, `POST /agent/register` returns a token.
- [ ] `POST /agent/snapshot` with the contract payload writes rows into `tasks` and `cp_events`.
- [ ] `POST /agent/heartbeat` updates `actor_presence`.

## Backup

`deploy/backup.sh` is intended for daily cron:

```
0 3 * * * /opt/wily-board/deploy/backup.sh
```
```

- [ ] **Step 3: Commit**

```bash
git add README.md docs/deploy.md
git commit -m "docs: README + deployment runbook"
```

---

## Plan 1 Complete

At this point:
- `wily-board` runs locally (`uv run uvicorn app.main:app --reload`)
- All `/agent/*` endpoints accept payloads matching `tests/contracts/agent_v1.json` and write the full v3 data model (including parallel meta, cp_events, observed_commits, task_results)
- GitHub OAuth + R-W-LAB allowlist gate web access
- Deploy scripts ready for the Azure VM
- No UI cards, no SSE, no real-time browser updates (Plan 3)
- No wily-agent daemon yet (Plan 2)
