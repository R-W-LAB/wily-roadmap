"""Git observation helpers for Wily v3."""

from __future__ import annotations

import fnmatch
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from .models import Actor, Task


@dataclass
class CommitInfo:
    sha: str
    author_email: str
    author_name: str
    subject: str
    body: str
    trailers: dict[str, str] = field(default_factory=dict)
    files: list[str] = field(default_factory=list)


def _git(cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=check,
    )


def head_sha(repo: Path) -> str:
    return _git(repo, "rev-parse", "HEAD").stdout.strip()


def initial_commit(repo: Path) -> str:
    out = _git(repo, "rev-list", "--max-parents=0", "HEAD").stdout.strip()
    return out.splitlines()[0] if out else head_sha(repo)


def observation_base(repo: Path) -> str:
    branch = _git(repo, "branch", "--show-current", check=False).stdout.strip()
    if branch:
        remote_ref = f"origin/{branch}"
        result = _git(repo, "rev-parse", "--verify", remote_ref, check=False)
        if result.returncode == 0 and result.stdout.strip():
            return remote_ref
    return head_sha(repo)


def fetch_observation_remote(repo: Path) -> str | None:
    branch = _git(repo, "branch", "--show-current", check=False).stdout.strip()
    if not branch:
        return None
    remote_check = _git(repo, "remote", "get-url", "origin", check=False)
    if remote_check.returncode != 0:
        return None
    _git(repo, "fetch", "origin", branch, check=False)
    remote_ref = f"origin/{branch}"
    result = _git(repo, "rev-parse", "--verify", remote_ref, check=False)
    if result.returncode == 0 and result.stdout.strip():
        return remote_ref
    return None


def changed_files_since(repo: Path, sha: str) -> list[str]:
    out = _git(repo, "diff", "--name-only", f"{sha}...HEAD").stdout
    return [line for line in out.splitlines() if line.strip()]


def changed_files_since_by_actor(repo: Path, sha: str, *, actor: Actor | None) -> list[str]:
    if actor is None:
        return changed_files_since(repo, sha)
    files: list[str] = []
    seen: set[str] = set()
    for commit in list_commits_since_fork(repo, sha, limit=200):
        if not actor.matches(email=commit.author_email, name=commit.author_name):
            continue
        for file in commit.files:
            if file not in seen:
                seen.add(file)
                files.append(file)
    return files


def parse_trailers(message: str) -> dict[str, str]:
    lines = message.rstrip().splitlines()
    block: list[str] = []
    for line in reversed(lines):
        if not line.strip() or ":" not in line:
            break
        key, _, value = line.partition(":")
        if not key or any(ch.isspace() for ch in key):
            break
        block.append(f"{key.strip()}: {value.strip()}")
    trailers: dict[str, str] = {}
    for entry in block:
        key, _, value = entry.partition(":")
        trailers[key] = value
    return trailers


def match_actor(actors: Iterable[Actor], *, email: str, name: str) -> Actor | None:
    for actor in actors:
        if actor.matches(email=email, name=name):
            return actor
    return None


def guess_task_id(tasks: Iterable[Task], changed_files: list[str]) -> str | None:
    scores: dict[str, int] = {}
    for task in tasks:
        if not task.scope:
            continue
        hits = 0
        for file in changed_files:
            if any(fnmatch.fnmatch(file, pattern) for pattern in task.scope):
                hits += 1
        if hits:
            scores[task.id] = hits
    if not scores:
        return None
    return max(scores.items(), key=lambda item: item[1])[0]


def list_commits_since_fork(repo: Path, base_sha: str, *, limit: int = 50) -> list[CommitInfo]:
    return _list_commits_in_range(repo, f"{base_sha}..HEAD", limit=limit)


def list_remote_commits(repo: Path, remote_ref: str, *, limit: int = 50) -> list[CommitInfo]:
    return _list_commits_in_range(repo, f"HEAD..{remote_ref}", limit=limit)


def _list_commits_in_range(repo: Path, rev_range: str, *, limit: int = 50) -> list[CommitInfo]:
    result = _git(
        repo,
        "log",
        f"--max-count={limit}",
        "--pretty=format:%H%x1f%ae%x1f%an%x1f%s%x1f%b%x1e",
        rev_range,
        check=False,
    )
    if result.returncode != 0:
        return []
    commits: list[CommitInfo] = []
    for record in result.stdout.split("\x1e"):
        record = record.strip("\n")
        if not record:
            continue
        parts = record.split("\x1f")
        if len(parts) < 5:
            continue
        sha, email, name, subject, body = parts[:5]
        message = f"{subject}\n\n{body}" if body else subject
        files_out = _git(repo, "show", "--name-only", "--pretty=format:", sha, check=False)
        files = [line for line in files_out.stdout.splitlines() if line.strip()]
        commits.append(
            CommitInfo(
                sha=sha,
                author_email=email,
                author_name=name,
                subject=subject,
                body=body,
                trailers=parse_trailers(message),
                files=files,
            )
        )
    return commits


def git_config_identity(repo: Path) -> tuple[str, str]:
    email = _git(repo, "config", "user.email", check=False).stdout.strip()
    name = _git(repo, "config", "user.name", check=False).stdout.strip()
    return email, name
