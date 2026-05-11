from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "wily.py"


class WilyCliTest(unittest.TestCase):
    def run_wily(self, project: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=project,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def create_state(self, project: Path) -> Path:
        state = project / ".wily"
        for name in ("phases", "sessions", "revisions"):
            (state / name).mkdir(parents=True, exist_ok=True)
        (state / "project.md").write_text("# Wily Project\n", encoding="utf-8")
        (state / "status.md").write_text("# Wily Status\n", encoding="utf-8")
        (state / "decisions.md").write_text("# Wily Decisions\n", encoding="utf-8")
        return state

    def write_ready_phase(self, project: Path) -> None:
        self.create_state(project)
        phase_dir = project / ".wily" / "phases" / "01-first-phase"
        phase_dir.mkdir(parents=True, exist_ok=True)
        (phase_dir / "phase.md").write_text("# Phase\n\nRoadmap-level phase definition\n", encoding="utf-8")
        (phase_dir / "prompt.md").write_text("Run this phase\n", encoding="utf-8")
        (phase_dir / "verification.md").write_text("python3 -m unittest\n", encoding="utf-8")
        (phase_dir / "handoff.md").write_text("Resume from here\n", encoding="utf-8")
        (phase_dir / "planner.md").write_text(
            "\n".join(
                [
                    "# Planner Adapter",
                    "",
                    "Recommended planner: superpowers:writing-plans",
                    "",
                    "Use this planner to create the implementation plan.",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (project / ".wily" / "roadmap.yaml").write_text(
            "\n".join(
                [
                    'roadmap_version: 1',
                    'goal: "Ship useful app"',
                    'phases:',
                    '  - id: "01"',
                    '    title: "First phase"',
                    '    path: "phases/01-first-phase"',
                    '    status: "ready"',
                    '    depends_on: []',
                ]
            ),
            encoding="utf-8",
        )

    def test_init_creates_wily_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)

            result = self.run_wily(project, "init", "Ship useful app")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Initialized .wily", result.stdout)
            self.assertTrue((project / ".wily" / "project.md").is_file())
            self.assertTrue((project / ".wily" / "roadmap.yaml").is_file())
            self.assertTrue((project / ".wily" / "status.md").is_file())
            self.assertTrue((project / ".wily" / "decisions.md").is_file())
            self.assertTrue((project / ".wily" / "phases").is_dir())
            self.assertTrue((project / ".wily" / "sessions").is_dir())
            self.assertTrue((project / ".wily" / "revisions").is_dir())
            self.assertIn("Ship useful app", (project / ".wily" / "project.md").read_text(encoding="utf-8"))

    def test_status_uses_roadmap_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.create_state(project)
            (project / ".wily" / "roadmap.yaml").write_text(
                "\n".join(
                    [
                        'roadmap_version: 1',
                        'goal: "Ship useful app"',
                        'phases:',
                        '  - id: "01"',
                        '    title: "First phase"',
                        '    path: "phases/01-first-phase"',
                        '    status: "ready"',
                        '    depends_on: []',
                        '    parallel_group: null',
                    ]
                ),
                encoding="utf-8",
            )

            result = self.run_wily(project, "status")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Roadmap version: 1", result.stdout)
            self.assertIn("Next: 01 - First phase", result.stdout)

    def test_next_prints_ready_phase_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.create_state(project)
            phase_dir = project / ".wily" / "phases" / "01-first-phase"
            phase_dir.mkdir(parents=True)
            (phase_dir / "phase.md").write_text("# Phase\n\nPurpose text\n", encoding="utf-8")
            (phase_dir / "plan.md").write_text("# Plan\n\nStep text\n", encoding="utf-8")
            (phase_dir / "prompt.md").write_text("Run this phase\n", encoding="utf-8")
            (phase_dir / "verification.md").write_text("python3 -m unittest\n", encoding="utf-8")
            (project / ".wily" / "roadmap.yaml").write_text(
                "\n".join(
                    [
                        'roadmap_version: 1',
                        'phases:',
                        '  - id: "01"',
                        '    title: "First phase"',
                        '    path: "phases/01-first-phase"',
                        '    status: "ready"',
                        '    depends_on: []',
                    ]
                ),
                encoding="utf-8",
            )

            result = self.run_wily(project, "next")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Next phase: 01 - First phase", result.stdout)
            self.assertIn("## Phase", result.stdout)
            self.assertIn("Purpose text", result.stdout)
            self.assertIn("## Existing Implementation Plan", result.stdout)
            self.assertIn("Step text", result.stdout)
            self.assertIn("## Prompt", result.stdout)
            self.assertIn("Run this phase", result.stdout)
            self.assertIn("## Verification", result.stdout)
            self.assertIn("python3 -m unittest", result.stdout)

    def test_next_prints_planner_handoff_and_optional_plan_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.write_ready_phase(project)

            result = self.run_wily(project, "next")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("## Planner Adapter", result.stdout)
            self.assertIn("Recommended planner: superpowers:writing-plans", result.stdout)
            self.assertIn("## Handoff", result.stdout)
            self.assertIn("Resume from here", result.stdout)
            self.assertIn("## Existing Implementation Plan", result.stdout)
            self.assertIn("No implementation plan exists yet.", result.stdout)

    def test_replan_records_revision_and_increments_version(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.create_state(project)
            (project / ".wily" / "roadmap.yaml").write_text(
                "\n".join(
                    [
                        'roadmap_version: 1',
                        'goal: "Ship useful app"',
                        'phases:',
                        '  - id: "01"',
                        '    title: "Finished work"',
                        '    path: "phases/01-finished-work"',
                        '    status: "done"',
                        '    depends_on: []',
                        '',
                        '  - id: "02"',
                        '    title: "Future work"',
                        '    path: "phases/02-future-work"',
                        '    status: "pending"',
                        '    depends_on: ["01"]',
                    ]
                ),
                encoding="utf-8",
            )

            result = self.run_wily(project, "replan", "Switch target")

            self.assertEqual(result.returncode, 0, result.stderr)
            roadmap = (project / ".wily" / "roadmap.yaml").read_text(encoding="utf-8")
            self.assertIn("roadmap_version: 2", roadmap)
            self.assertIn('status: "done"', roadmap)
            revisions = sorted((project / ".wily" / "revisions").glob("*.md"))
            self.assertEqual(len(revisions), 1)
            self.assertIn("Switch target", revisions[0].read_text(encoding="utf-8"))

    def test_start_creates_session_and_marks_phase_in_progress(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.write_ready_phase(project)

            result = self.run_wily(project, "start", "01")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Started phase 01", result.stdout)
            sessions = sorted((project / ".wily" / "sessions").glob("*phase-01-attempt-1"))
            self.assertEqual(len(sessions), 1)
            session = sessions[0]
            self.assertTrue((session / "status.yaml").is_file())
            self.assertTrue((session / "input.md").is_file())
            self.assertTrue((session / "result.md").is_file())
            self.assertTrue((session / "verification.md").is_file())
            self.assertTrue((session / "changed-files.md").is_file())
            roadmap = (project / ".wily" / "roadmap.yaml").read_text(encoding="utf-8")
            self.assertIn('status: "in_progress"', roadmap)
            self.assertIn('current_session: "sessions/', roadmap)

    def test_start_writes_external_planner_context_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.write_ready_phase(project)
            phase_dir = project / ".wily" / "phases" / "01-first-phase"
            (phase_dir / "plan.md").write_text("External generated plan\n", encoding="utf-8")

            result = self.run_wily(project, "start", "01")

            self.assertEqual(result.returncode, 0, result.stderr)
            sessions = sorted((project / ".wily" / "sessions").glob("*phase-01-attempt-1"))
            self.assertEqual(len(sessions), 1)
            input_text = (sessions[0] / "input.md").read_text(encoding="utf-8")
            self.assertIn("# Wily Phase Context", input_text)
            self.assertIn("## Phase", input_text)
            self.assertIn("Roadmap-level phase definition", input_text)
            self.assertIn("## Planner Adapter", input_text)
            self.assertIn("Recommended planner: superpowers:writing-plans", input_text)
            self.assertIn("## Prompt", input_text)
            self.assertIn("Run this phase", input_text)
            self.assertIn("## Verification", input_text)
            self.assertIn("python3 -m unittest", input_text)
            self.assertIn("## Handoff", input_text)
            self.assertIn("Resume from here", input_text)
            self.assertIn("## Existing Implementation Plan", input_text)
            self.assertIn("External generated plan", input_text)

    def test_start_records_recommended_planner_in_session_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.write_ready_phase(project)

            result = self.run_wily(project, "start", "01")

            self.assertEqual(result.returncode, 0, result.stderr)
            status_files = list((project / ".wily" / "sessions").glob("*phase-01-attempt-1/status.yaml"))
            self.assertEqual(len(status_files), 1)
            status_text = status_files[0].read_text(encoding="utf-8")
            self.assertIn('planner: "superpowers:writing-plans"', status_text)

    def test_start_allows_missing_implementation_plan(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.write_ready_phase(project)

            result = self.run_wily(project, "start", "01")

            self.assertEqual(result.returncode, 0, result.stderr)
            sessions = sorted((project / ".wily" / "sessions").glob("*phase-01-attempt-1"))
            self.assertEqual(len(sessions), 1)
            input_text = (sessions[0] / "input.md").read_text(encoding="utf-8")
            self.assertIn("## Existing Implementation Plan", input_text)
            self.assertIn("No implementation plan exists yet.", input_text)
            self.assertIn("Use the recommended planner to create one if this phase needs a detailed plan.", input_text)

    def test_complete_marks_phase_done_and_session_verified(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.write_ready_phase(project)
            self.run_wily(project, "start", "01")

            result = self.run_wily(project, "complete", "01")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Completed phase 01", result.stdout)
            roadmap = (project / ".wily" / "roadmap.yaml").read_text(encoding="utf-8")
            self.assertIn('status: "done"', roadmap)
            status_files = list((project / ".wily" / "sessions").glob("*phase-01-attempt-1/status.yaml"))
            self.assertEqual(len(status_files), 1)
            self.assertIn('status: "verified"', status_files[0].read_text(encoding="utf-8"))

    def test_block_marks_phase_blocked_and_records_reason(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.write_ready_phase(project)
            self.run_wily(project, "start", "01")

            result = self.run_wily(project, "block", "01", "Permission missing")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Blocked phase 01", result.stdout)
            roadmap = (project / ".wily" / "roadmap.yaml").read_text(encoding="utf-8")
            self.assertIn('status: "blocked"', roadmap)
            self.assertIn('blocker: "Permission missing"', roadmap)
            status_files = list((project / ".wily" / "sessions").glob("*phase-01-attempt-1/status.yaml"))
            self.assertEqual(len(status_files), 1)
            self.assertIn('status: "blocked"', status_files[0].read_text(encoding="utf-8"))
            self.assertIn('blocker: "Permission missing"', status_files[0].read_text(encoding="utf-8"))

    def test_retry_creates_next_attempt_and_preserves_previous_session(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.write_ready_phase(project)
            self.run_wily(project, "start", "01")
            self.run_wily(project, "block", "01", "Permission missing")

            result = self.run_wily(project, "retry", "01")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Started phase 01 attempt 2", result.stdout)
            self.assertEqual(len(list((project / ".wily" / "sessions").glob("*phase-01-attempt-1"))), 1)
            self.assertEqual(len(list((project / ".wily" / "sessions").glob("*phase-01-attempt-2"))), 1)
            roadmap = (project / ".wily" / "roadmap.yaml").read_text(encoding="utf-8")
            self.assertIn('status: "in_progress"', roadmap)
            self.assertIn('current_session: "sessions/', roadmap)


if __name__ == "__main__":
    unittest.main()
