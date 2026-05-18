"""`wily land <id>` - commit local task changes with a Wily trailer."""

from __future__ import annotations

import fnmatch
import subprocess
import sys
from pathlib import Path

from ..config import load_tasks
from ..models import TaskStatus
from ..paths import WilyPaths, WilyRootNotFound, find_wily_root
from . import _common


def main(args: list[str]) -> int:
    force = "--force" in args
    no_push = "--no-push" in args
    positional = [arg for arg in args if not arg.startswith("--")]
    if len(positional) != 1:
        _common.emit_error("usage: wily land <task-id> [--no-push] [--force]")
        return _common.EXIT_USAGE
    task_id = positional[0]
    try:
        root = find_wily_root(Path.cwd())
    except WilyRootNotFound as exc:
        _common.emit_error(str(exc))
        return _common.EXIT_FAILURE
    paths = WilyPaths(root)
    _, tasks = load_tasks(paths)
    task = next((item for item in tasks if item.id == task_id), None)
    if task is None:
        _common.emit_error(f"task not found: {task_id}")
        return _common.EXIT_FAILURE
    if task.status != TaskStatus.DONE and not force:
        _common.emit_error(f"{task_id} is {task.status.value}; run wily done first")
        return _common.EXIT_TRANSITION
    changed = _changed(root)
    if not changed:
        _common.emit_error("nothing to commit")
        return _common.EXIT_FAILURE
    in_scope, out_scope = _split(changed, task.scope)
    files = changed if force or not out_scope else in_scope
    if out_scope and not force:
        _common.emit_text(f"warning: {len(out_scope)} file(s) outside scope; use --force to include")
    if not files:
        _common.emit_error("no in-scope files to commit")
        return _common.EXIT_FAILURE
    subprocess.run(["git", "add", *files], cwd=root, check=True)
    subprocess.run(["git", "commit", "-m", _message(paths, task.id, task.title)], cwd=root, check=True)
    _common.emit_text(f"committed: {task.id}: {task.title}")
    if no_push:
        _common.emit_text("(push skipped: --no-push)")
        return _common.EXIT_OK
    if not _confirm("push to origin? [y/N] "):
        _common.emit_text("(push skipped)")
        return _common.EXIT_OK
    return _common.EXIT_OK if _do_push(root) else _common.EXIT_FAILURE


def _changed(root: Path) -> list[str]:
    out = subprocess.run(["git", "status", "--porcelain"], cwd=root, capture_output=True, text=True, check=True).stdout
    files: list[str] = []
    for line in out.splitlines():
        if line.strip():
            files.append(line[3:])
    return files


def _split(files: list[str], scope: list[str]) -> tuple[list[str], list[str]]:
    if not scope:
        return files, []
    inside = [file for file in files if any(fnmatch.fnmatch(file, pattern) for pattern in scope)]
    outside = [file for file in files if file not in inside]
    return inside, outside


def _message(paths: WilyPaths, task_id: str, title: str) -> str:
    body = ""
    result = paths.result_md(task_id)
    if result.exists():
        bullets = [line for line in result.read_text(encoding="utf-8").splitlines() if line.startswith("- ")]
        body = "\n".join(bullets[:6])
    return f"{task_id}: {title}\n\n{body}\n\nWily-Task: {task_id}\n"


def _confirm(prompt: str) -> bool:
    sys.stdout.write(prompt)
    sys.stdout.flush()
    return sys.stdin.readline().strip().lower() in {"y", "yes"}


def _do_push(root: Path) -> bool:
    return subprocess.run(["git", "push"], cwd=root, check=False).returncode == 0
