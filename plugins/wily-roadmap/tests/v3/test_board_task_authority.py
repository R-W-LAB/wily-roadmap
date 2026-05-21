from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from wily.agent.config import AgentConfig, load_config, save_config  # noqa: E402
from wily.agent.config import default_paths  # noqa: E402
from wily.cli import agent as agent_cmd  # noqa: E402
from wily.cli import block as block_cmd, claim as claim_cmd, cp as cp_cmd, done as done_cmd, next as next_cmd  # noqa: E402
from wily.config import load_tasks, save_actors, save_tasks  # noqa: E402
from wily.models import Actor, Task, TaskStatus  # noqa: E402
from wily.paths import WilyPaths  # noqa: E402
from wily.progress import read_events  # noqa: E402


class chdir_compat:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.old: str | None = None

    def __enter__(self) -> None:
        self.old = os.getcwd()
        os.chdir(self.path)

    def __exit__(self, *_exc) -> None:
        if self.old is not None:
            os.chdir(self.old)


class BoardTaskAuthorityCliTest(unittest.TestCase):
    def test_claim_uses_board_and_refreshes_local_runtime_fields(self) -> None:
        with configured_repo([Task(id="T01", title="First", intent="do", acceptance="done")]) as root:
            paths = WilyPaths(root)
            response = runtime_response("T01", status="in_progress", actor="wily", claim_sha="board-sha")

            with chdir_compat(root), patch("wily.board_runtime.transition_task", return_value=response) as transition:
                self.assertEqual(claim_cmd.main(["T01", "--as", "wily"]), 0)

            transition.assert_called_once()
            _, _, task_id, action, payload = transition.call_args.args
            self.assertEqual((task_id, action), ("T01", "claim"))
            self.assertTrue(payload["claim_sha"])
            tasks = load_tasks(paths)[1]
            self.assertEqual(tasks[0].status, TaskStatus.IN_PROGRESS)
            self.assertEqual(tasks[0].actor, "wily")
            self.assertEqual(tasks[0].claim_sha, "board-sha")
            self.assertTrue(paths.progress_jsonl("T01").exists())

    def test_claim_board_failure_does_not_mutate_local_task(self) -> None:
        with configured_repo([Task(id="T01", title="First", intent="do", acceptance="done")]) as root:
            paths = WilyPaths(root)

            with chdir_compat(root), patch(
                "wily.board_runtime.transition_task",
                return_value={"sent": False, "reason": "board down"},
            ), redirect_stderr(StringIO()) as stderr:
                code = claim_cmd.main(["T01", "--as", "wily"])

            self.assertEqual(code, 1)
            self.assertIn("Board task authority failed", stderr.getvalue())
            self.assertEqual(load_tasks(paths)[1][0].status, TaskStatus.READY)
            self.assertFalse(paths.progress_jsonl("T01").exists())

    def test_next_refreshes_board_runtime_before_selecting_task(self) -> None:
        with configured_repo(
            [
                Task(id="T01", title="First", intent="do", acceptance="done"),
                Task(id="T02", title="Second", intent="do", acceptance="done"),
            ]
        ) as root:
            paths = WilyPaths(root)
            board_tasks = [
                runtime_response("T01", status="done", actor="wily"),
                runtime_response("T02", status="ready"),
            ]

            with chdir_compat(root), patch(
                "wily.board_runtime.list_project_tasks",
                return_value={"sent": True, "tasks": board_tasks},
            ), redirect_stdout(StringIO()) as stdout:
                self.assertEqual(next_cmd.main(["--json"]), 0)

            payload = json.loads(stdout.getvalue())
            self.assertEqual(payload["id"], "T02")
            self.assertEqual(load_tasks(paths)[1][0].status, TaskStatus.DONE)

    def test_cp_board_failure_does_not_append_local_progress(self) -> None:
        with configured_repo([Task(id="T01", title="First", status=TaskStatus.IN_PROGRESS, actor="wily")]) as root:
            paths = WilyPaths(root)

            with chdir_compat(root), patch(
                "wily.board_runtime.transition_task",
                return_value={"sent": False, "reason": "board down"},
            ):
                code = cp_cmd.main(["T01", "start", "Implementation", "--actor", "wily", "--ts", "2026-05-21T00:00:00Z"])

            self.assertEqual(code, 1)
            self.assertEqual(read_events(paths, "T01"), [])

    def test_done_board_failure_does_not_write_result_or_mark_done(self) -> None:
        with configured_repo([Task(id="T01", title="First", status=TaskStatus.IN_PROGRESS, actor="wily", claim_sha="seed")]) as root:
            paths = WilyPaths(root)

            with chdir_compat(root), patch(
                "wily.board_runtime.transition_task",
                return_value={"sent": False, "reason": "board down"},
            ):
                code = done_cmd.main(["T01", "--force"])

            self.assertEqual(code, 1)
            self.assertEqual(load_tasks(paths)[1][0].status, TaskStatus.IN_PROGRESS)
            self.assertFalse(paths.result_md("T01").exists())

    def test_block_uses_board_and_refreshes_local_runtime_fields(self) -> None:
        with configured_repo([Task(id="T01", title="First")]) as root:
            paths = WilyPaths(root)

            with chdir_compat(root), patch(
                "wily.board_runtime.transition_task",
                return_value=runtime_response("T01", status="blocked", actor="wily", blocker="waiting"),
            ):
                self.assertEqual(block_cmd.main(["T01", "waiting"]), 0)

            task = load_tasks(paths)[1][0]
            self.assertEqual(task.status, TaskStatus.BLOCKED)
            self.assertEqual(task.blocker, "waiting")

    def test_agent_configure_preserves_task_authority_flag(self) -> None:
        with configured_repo([Task(id="T01", title="First")]) as _root:
            self.assertEqual(agent_cmd.main(["configure", "--repo", "R-W-LAB/other"]), 0)
            config = load_config(default_paths().config_path)

        self.assertTrue(config.task_authority)
        self.assertEqual(config.repo, "R-W-LAB/other")


def configured_repo(tasks: list[Task]):
    return _ConfiguredRepo(tasks)


class _ConfiguredRepo:
    def __init__(self, tasks: list[Task]) -> None:
        self.tasks = tasks
        self.tmp: tempfile.TemporaryDirectory[str] | None = None
        self.env_patch = None

    def __enter__(self) -> Path:
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        _git_repo(root)
        paths = WilyPaths(root)
        paths.wily_dir.mkdir()
        save_actors(paths, [Actor(id="wily", display="Wily", git_author_emails=["wily@example.com"])])
        save_tasks(paths, "demo", self.tasks)
        config_path = root / "agent-config.json"
        save_config(
            config_path,
            AgentConfig(
                board_url="https://board.example",
                repo="R-W-LAB/demo",
                actor="wily",
                token="token",
                machine_id="machine-1",
                task_authority=True,
            ),
        )
        self.env_patch = patch.dict(os.environ, {"WILY_AGENT_CONFIG": str(config_path)})
        self.env_patch.__enter__()
        return root

    def __exit__(self, *_exc) -> None:
        if self.env_patch is not None:
            self.env_patch.__exit__(*_exc)
        if self.tmp is not None:
            self.tmp.cleanup()


def runtime_response(
    task_id: str,
    *,
    status: str,
    actor: str | None = None,
    claim_sha: str | None = None,
    blocker: str | None = None,
) -> dict[str, object]:
    return {
        "sent": True,
        "project_id": "R-W-LAB/demo",
        "task_id": task_id,
        "status": status,
        "ui_status": "working" if status == "in_progress" else status,
        "owner": actor,
        "actor": actor,
        "claim_sha": claim_sha,
        "claim_at": "2026-05-21T00:00:00Z" if status == "in_progress" else None,
        "done_at": "2026-05-21T00:02:00Z" if status == "done" else None,
        "blocker": blocker,
        "progress": {"done": 0, "total": 0, "current_cp": None},
        "checkpoints": [],
    }


def _git_repo(path: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.email", "wily@example.com"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.name", "wily"], cwd=path, check=True)
    (path / "README.md").write_text("# demo\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=path, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "seed"], cwd=path, check=True)


if __name__ == "__main__":
    unittest.main()
