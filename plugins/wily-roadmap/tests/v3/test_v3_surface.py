from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MARKETPLACE = ROOT.parents[1] / ".agents" / "plugins" / "marketplace.json"

COMMANDS = {"init", "next", "claim", "go", "done", "block", "replan", "land", "watch", "status"}
SKILLS = {f"wily-{name}" for name in COMMANDS} | {"wily-execute"}


class V3SurfaceTest(unittest.TestCase):
    def test_plugin_manifest_exposes_v3_only(self) -> None:
        data = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual({item["name"] for item in data["commands"]}, COMMANDS)
        self.assertEqual({item["name"] for item in data["skills"]}, SKILLS)
        self.assertNotIn("board", json.dumps(data).lower())
        self.assertNotIn("stage", json.dumps(data).lower())

    def test_marketplace_points_to_plugin(self) -> None:
        data = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
        plugin = data["plugins"][0]
        self.assertEqual(plugin["source"]["path"], "./plugins/wily-roadmap")
        self.assertEqual(plugin["version"], "3.0.0")

    def test_skill_directories_are_exactly_v3(self) -> None:
        dirs = {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()}
        self.assertEqual(dirs, SKILLS)
        execute = (ROOT / "skills" / "wily-execute" / "SKILL.md").read_text(encoding="utf-8")
        for token in ("wily claim", "wily go", "custom-workflow-skillset:plan-goal-runner", "wily done"):
            self.assertIn(token, execute)

    def test_v2_runtime_files_are_removed(self) -> None:
        removed = {
            ROOT / "scripts" / "wily_state_summary.py",
            ROOT / "scripts" / "wily_watch_ui.py",
            ROOT / "scripts" / "wily_runner.py",
            ROOT / "scripts" / "wily_projection.py",
            ROOT / "tests" / "test_wily_cli.py",
            ROOT / "tests" / "test_wily_command_skills.py",
            ROOT / "tests" / "test_wily_state_summary.py",
            ROOT / "tests" / "test_wily_watch_ui.py",
        }
        for path in removed:
            with self.subTest(path=path):
                self.assertFalse(path.exists())

    def test_root_readme_documents_external_cleanup(self) -> None:
        readme = (ROOT.parents[1] / "README.md").read_text(encoding="utf-8")
        self.assertIn("~/.codex/hooks.json", readme)
        self.assertIn(".github/workflows/wily-" + "board-sync.yml", readme)
        self.assertIn("~/.wily/board.json", readme)


if __name__ == "__main__":
    unittest.main()
