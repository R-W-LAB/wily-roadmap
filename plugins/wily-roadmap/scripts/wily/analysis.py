"""Best-effort brownfield repository analysis for `wily init --adopt`."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class BrownfieldSnapshot:
    commit_count: int = 0
    authors: list[dict] = field(default_factory=list)
    readme_excerpt: str | None = None
    top_level_files: list[str] = field(default_factory=list)
    legacy_wily_detected: bool = False


def analyze_repo(repo: Path) -> BrownfieldSnapshot:
    return BrownfieldSnapshot(
        commit_count=_commit_count(repo),
        authors=extract_authors(repo),
        readme_excerpt=_read_readme(repo),
        top_level_files=_top_level(repo),
        legacy_wily_detected=_legacy_detected(repo),
    )


def extract_authors(repo: Path) -> list[dict]:
    result = subprocess.run(
        ["git", "log", "--pretty=format:%ae|%an", "HEAD"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    counts: dict[tuple[str, str], int] = {}
    for line in result.stdout.splitlines():
        if "|" not in line:
            continue
        email, name = line.split("|", 1)
        counts[(email, name)] = counts.get((email, name), 0) + 1
    return sorted(
        ({"email": email, "name": name, "commits": count} for (email, name), count in counts.items()),
        key=lambda item: -int(item["commits"]),
    )


def _commit_count(repo: Path) -> int:
    result = subprocess.run(
        ["git", "rev-list", "--count", "HEAD"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return 0
    try:
        return int(result.stdout.strip() or "0")
    except ValueError:
        return 0


def _read_readme(repo: Path) -> str | None:
    for name in ("README.md", "README.rst", "README.txt", "README"):
        path = repo / name
        if path.exists():
            return "\n".join(path.read_text(encoding="utf-8", errors="replace").splitlines()[:30])
    return None


def _top_level(repo: Path) -> list[str]:
    try:
        return sorted(p.name for p in repo.iterdir() if not p.name.startswith("."))
    except OSError:
        return []


def _legacy_detected(repo: Path) -> bool:
    if (repo / ".wily" / "roadmap.yaml").exists():
        return True
    archive = repo / ".wily" / "archive"
    if not archive.exists():
        return False
    return any(path.name == "roadmap.yaml" for path in archive.glob("legacy-*/roadmap.yaml"))
