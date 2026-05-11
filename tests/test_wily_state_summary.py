from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "wily_state_summary.py"


class WilyStateSummaryTest(unittest.TestCase):
    def run_summary(self, project: Path) -> str:
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=project,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_reports_no_state_without_wily_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            output = self.run_summary(project)

        self.assertIn("State: none", output)
        self.assertIn("Git: not a git repo", output)

    def test_summarizes_ready_and_blocked_phases(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / ".git").mkdir()
            (project / ".wily").mkdir()
            (project / ".wily" / "roadmap.yaml").write_text(
                "\n".join(
                    [
                        'roadmap_version: 1',
                        'goal: "Ship release-ready app"',
                        'phases:',
                        '  - id: "01"',
                        '    title: "Audit current implementation"',
                        '    path: "phases/01-audit"',
                        '    status: "done"',
                        '    depends_on: []',
                        '    parallel_group: null',
                        '',
                        '  - id: "02"',
                        '    title: "Core engine"',
                        '    path: "phases/02-core-engine"',
                        '    status: "ready"',
                        '    depends_on: ["01"]',
                        '    parallel_group: null',
                        '',
                        '  - id: "03"',
                        '    title: "Packaging"',
                        '    path: "phases/03-packaging"',
                        '    status: "blocked"',
                        '    depends_on: ["02"]',
                        '    parallel_group: null',
                    ]
                ),
                encoding="utf-8",
            )

            output = self.run_summary(project)

        self.assertIn("State: .wily", output)
        self.assertIn("Roadmap version: 1", output)
        self.assertIn("Progress: 1 done, 1 ready, 0 in progress, 1 blocked, 0 superseded", output)
        self.assertIn("Next: 02 - Core engine", output)
        self.assertIn("Ready phases:", output)
        self.assertIn("  - 02 Core engine", output)
        self.assertIn("Blocked phases:", output)
        self.assertIn("  - 03 Packaging (depends on: 02)", output)

    def test_summarizes_superseded_replacement_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / ".wily").mkdir()
            (project / ".wily" / "roadmap.yaml").write_text(
                "\n".join(
                    [
                        'roadmap_version: 2',
                        'phases:',
                        '  - id: "04"',
                        '    title: "Old integration plan"',
                        '    path: "phases/04-old-integration"',
                        '    status: "superseded"',
                        '    depends_on: ["03"]',
                        '    parallel_group: null',
                        '',
                        '  - id: "04R"',
                        '    title: "Adapt foundation"',
                        '    path: "phases/04r-adapt-foundation"',
                        '    status: "ready"',
                        '    depends_on: ["03"]',
                        '    replaces: ["04"]',
                    ]
                ),
                encoding="utf-8",
            )

            output = self.run_summary(project)

        self.assertIn("Roadmap version: 2", output)
        self.assertIn("Next: 04R - Adapt foundation", output)
        self.assertIn("Replacements:", output)
        self.assertIn("  - 04R replaces 04", output)
        self.assertIn("Superseded phases:", output)
        self.assertIn("  - 04 Old integration plan", output)


if __name__ == "__main__":
    unittest.main()
