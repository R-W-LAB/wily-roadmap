"""`wily workspace` - manifest-only multi-repo views."""

from __future__ import annotations

import time
from pathlib import Path

import yaml

from ..workspace import (
    SCHEMA_VERSION,
    WorkspaceConfig,
    WorkspaceManifestError,
    WorkspaceRepo,
    discover_workspace_manifest,
    load_workspace,
    workspace_snapshot,
)
from . import _common

DESCRIPTION = "print manifest-only multi-repo workspace views"
USAGE = "usage: wily workspace <init|show-config|status|next|watch> [args]"
HELP = "\n".join(
    [
        "Commands:",
        "  init --repo <id=path> [--repo <id=path> ...] [--title <text>]",
        "  show-config [--json]",
        "  status [--json] [--repo <id>] [--group <group>]",
        "  next [--json] [--repo <id>] [--group <group>]",
        "  watch [--once] [--interval <seconds>] [--json] [--repo <id>] [--group <group>]",
        "",
        "The workspace manifest is configuration only. Child repos keep their own .wily/tasks.yaml source of truth.",
    ]
)


def main(args: list[str]) -> int:
    if not args:
        _common.emit_error(USAGE)
        return _common.EXIT_USAGE
    subcommand, rest = args[0], args[1:]
    if subcommand == "init":
        return _init(rest)
    if subcommand == "show-config":
        return _show_config(rest)
    if subcommand == "status":
        return _status(rest)
    if subcommand == "next":
        return _next(rest)
    if subcommand == "watch":
        return _watch(rest)
    _common.emit_error(f"unknown workspace subcommand: {subcommand}")
    return _common.EXIT_USAGE


def _init(args: list[str]) -> int:
    if _common.missing_value_flag(args, {"--repo", "--title"}):
        _common.emit_error("usage: wily workspace init --repo <id=path> [--title <text>]")
        return _common.EXIT_USAGE
    repo_values = _common.extract_values(args, "--repo")
    if not repo_values:
        _common.emit_error("usage: wily workspace init --repo <id=path> [--repo <id=path> ...] [--title <text>]")
        return _common.EXIT_USAGE
    repos: list[dict[str, str]] = []
    for value in repo_values:
        if "=" not in value:
            _common.emit_error("--repo must use <id=path>")
            return _common.EXIT_USAGE
        repo_id, path = value.split("=", 1)
        repo_id = repo_id.strip()
        path = path.strip()
        if not repo_id or not path:
            _common.emit_error("--repo must use <id=path>")
            return _common.EXIT_USAGE
        repos.append({"id": repo_id, "path": path})
    title = _common.extract_value(args, "--title") or "Wily Workspace"
    manifest_path = Path.cwd() / "wily-workspace.yaml"
    payload = {"schema": SCHEMA_VERSION, "title": title, "repos": repos}
    manifest_path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    _common.emit_text(f"workspace manifest written: {manifest_path}")
    return _common.EXIT_OK


def _show_config(args: list[str]) -> int:
    args, as_json = _common.consume_json_flag(args)
    config = _load_filtered_workspace(args)
    if config is None:
        return _common.EXIT_FAILURE
    if as_json:
        _common.emit_json(config.to_dict())
    else:
        _common.emit_text(_render_config(config))
    return _common.EXIT_OK


def _status(args: list[str]) -> int:
    args, as_json = _common.consume_json_flag(args)
    config = _load_filtered_workspace(args)
    if config is None:
        return _common.EXIT_FAILURE
    snapshot = workspace_snapshot(config)
    if as_json:
        _common.emit_json(snapshot)
    else:
        _common.emit_text(render_workspace_status(snapshot))
    return _common.EXIT_OK


def _next(args: list[str]) -> int:
    args, as_json = _common.consume_json_flag(args)
    config = _load_filtered_workspace(args)
    if config is None:
        return _common.EXIT_FAILURE
    snapshot = workspace_snapshot(config)
    errors = _repo_errors(snapshot)
    tasks = _next_tasks_from_snapshot(snapshot)
    if not tasks:
        for error in errors:
            _common.emit_error(error)
        _common.emit_error("no ready task with satisfied dependencies in workspace")
        return _common.EXIT_FAILURE
    if as_json:
        _common.emit_json({"title": config.title, "tasks": tasks, "errors": errors})
    else:
        for error in errors:
            _common.emit_error(error)
        for task in tasks:
            _emit_workspace_task_line(task)
    return _common.EXIT_OK


def _watch(args: list[str]) -> int:
    args, as_json = _common.consume_json_flag(args)
    interval = _interval(args)
    if interval is None:
        return _common.EXIT_USAGE
    config = _load_filtered_workspace(args)
    if config is None:
        return _common.EXIT_FAILURE
    if "--once" in args or as_json:
        snapshot = workspace_snapshot(config)
        if as_json:
            _common.emit_json(snapshot)
        else:
            _common.emit_text(render_workspace_status(snapshot))
        return _common.EXIT_OK
    last_mtimes: tuple[int, ...] | None = None
    while True:
        current_mtimes = workspace_touch_mtimes(config)
        if last_mtimes is None or current_mtimes != last_mtimes:
            print("\033[2J\033[H", end="")
            _common.emit_text(render_workspace_status(workspace_snapshot(config)))
            last_mtimes = current_mtimes
        try:
            time.sleep(interval)
        except KeyboardInterrupt:
            return _common.EXIT_OK


def _load_filtered_workspace(args: list[str]) -> WorkspaceConfig | None:
    if _common.missing_value_flag(args, {"--repo", "--group", "--interval"}):
        _common.emit_error("missing value for workspace filter")
        return None
    try:
        config = load_workspace(discover_workspace_manifest(Path.cwd()))
    except WorkspaceManifestError as exc:
        _common.emit_error(str(exc))
        return None
    repo_id = _common.extract_value(args, "--repo")
    group = _common.extract_value(args, "--group")
    repos = [
        repo
        for repo in config.repos
        if (not repo_id or repo.id == repo_id) and (not group or repo.group == group)
    ]
    if repo_id and not repos:
        _common.emit_error(f"workspace repo not found: {repo_id}")
        return None
    if group and not repos:
        _common.emit_error(f"workspace group not found: {group}")
        return None
    return WorkspaceConfig(title=config.title, repos=repos, manifest_path=config.manifest_path)


def render_workspace_status(snapshot: dict[str, object]) -> str:
    lines = [
        f"Wily Workspace: {snapshot.get('title')}",
        f"Manifest: {snapshot.get('manifest_path')}",
        "",
    ]
    for repo in snapshot.get("repos") or []:
        if not isinstance(repo, dict):
            continue
        lines.extend(_render_repo(repo))
        lines.append("")
    return "\n".join(lines).rstrip()


def workspace_touch_mtimes(config: WorkspaceConfig) -> tuple[int, ...]:
    mtimes: list[int] = []
    for repo in config.repos:
        try:
            mtimes.append((repo.path / ".wily" / ".touch").stat().st_mtime_ns)
        except OSError:
            mtimes.append(0)
    return tuple(mtimes)


def _render_config(config: WorkspaceConfig) -> str:
    lines = [f"Workspace: {config.title}", f"Manifest: {config.manifest_path}", "Repos:"]
    for repo in config.repos:
        group = f" group={repo.group}" if repo.group else ""
        lines.append(f"  {repo.id} path={repo.path}{group}")
    return "\n".join(lines)


def _render_repo(repo: dict[str, object]) -> list[str]:
    if repo.get("error"):
        return [f"[{repo.get('id')}] ERROR {repo.get('error')}"]
    progress = repo.get("progress") if isinstance(repo.get("progress"), dict) else {}
    lines = [
        (
            f"[{repo.get('id')}] {repo.get('project_title') or repo.get('title') or repo.get('id')} "
            f"mode={repo.get('mode')} done={progress.get('done', 0)}/{progress.get('total', 0)} "
            f"ready={progress.get('ready', 0)} in_progress={progress.get('in_progress', 0)} blocked={progress.get('blocked', 0)}"
        )
    ]
    for label, key in (
        ("in-progress", "in_progress_tasks"),
        ("next", "next_tasks"),
        ("waiting", "waiting_tasks"),
        ("blocked", "blocked_tasks"),
    ):
        tasks = repo.get(key) or []
        if tasks:
            lines.append(f"  {label}:")
            for task in tasks:
                if isinstance(task, dict):
                    lines.append(f"    {task.get('id')} {task.get('title')}")
    return lines


def _next_tasks_from_snapshot(snapshot: dict[str, object]) -> list[dict[str, object]]:
    tasks: list[dict[str, object]] = []
    for repo in snapshot.get("repos") or []:
        if isinstance(repo, dict) and not repo.get("error"):
            tasks.extend(repo.get("next_tasks") or [])
    return tasks


def _repo_errors(snapshot: dict[str, object]) -> list[str]:
    errors: list[str] = []
    for repo in snapshot.get("repos") or []:
        if isinstance(repo, dict) and repo.get("error"):
            errors.append(f"[{repo.get('id')}] ERROR {repo.get('error')}")
    return errors


def _emit_workspace_task_line(task: dict[str, object]) -> None:
    deps = ",".join(str(dep) for dep in (task.get("depends_on") or [])) or "-"
    _common.emit_text(
        f"{task.get('repo_id')} {task.get('id')} ready  {task.get('title')!r}  "
        f"assignee={task.get('assignee') or '-'}  depends_on=[{deps}]"
    )


def _interval(args: list[str]) -> float | None:
    if "--interval" not in args:
        return 2.0
    value = _common.extract_value(args, "--interval")
    if value is None:
        _common.emit_error("--interval requires a value")
        return None
    try:
        interval = float(value)
    except ValueError:
        _common.emit_error("--interval value must be a number")
        return None
    if interval <= 0:
        _common.emit_error("--interval must be positive")
        return None
    return interval
