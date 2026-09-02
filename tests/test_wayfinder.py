from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from wayfinder.cli import main
from wayfinder.scanner import match_entities, scan_workspace


def make_workspace(root: Path, duplicate: bool = False, malformed: bool = False, broken: bool = False) -> None:
    (root / "AGENTS.md").write_text("# Root\n", encoding="utf-8")
    (root / "Development.manifest.toml").write_text(
        "[manifest]\nmanifest_type = 'workspace'\n[entity]\nid = 'development-drive'\ntitle = 'Development'\n[workspace]\nroot = 'fixture'\n[standards]\nwgs = 'standards/WGS'\ncts = 'standards/CTS'\n[[roots]]\npath = 'alpha'\nkind = 'portfolio'\n",
        encoding="utf-8",
    )
    (root / "standards" / "WGS").mkdir(parents=True, exist_ok=True)
    (root / "standards" / "WGS" / "README.md").write_text("# WGS\n", encoding="utf-8")
    (root / "alpha").mkdir(exist_ok=True)
    (root / "alpha" / "AGENTS.md").write_text("# Alpha\n", encoding="utf-8")
    (root / "alpha" / "Project-README.md").write_text("# Alpha\n", encoding="utf-8")
    broken_relationship = "[relationships]\nrelated_projects = ['missing-project']\n" if broken else ""
    (root / "alpha" / "Alpha.manifest.toml").write_text(
        "[manifest]\nmanifest_type = 'project'\n[entity]\nid = 'alpha'\ntitle = 'Alpha'\nkind = 'project'\n[lifecycle]\nstate = 'planning'\n[governance]\nprimary_standard = 'WGS'\n[agent]\nread_first = ['Project-README.md']\n" + broken_relationship,
        encoding="utf-8",
    )
    if duplicate:
        (root / "alpha" / "Beta.manifest.toml").write_text("[entity]\nid = 'alpha'\ntitle = 'Beta'\n", encoding="utf-8")
    if malformed:
        (root / "broken.manifest.toml").write_text("[entity\nid = 'broken'\n", encoding="utf-8")
    (root / "node_modules").mkdir(exist_ok=True)
    (root / "node_modules" / "Ignored.manifest.toml").write_text("[entity]\nid = 'ignored'\n", encoding="utf-8")


class WayfinderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        make_workspace(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_scan_is_sorted_and_excludes_generated_directories(self) -> None:
        scan = scan_workspace(self.root)
        self.assertEqual([entity.id for entity in scan.entities], ["alpha", "development-drive"])

    def test_resolve_matches_exact_identifier_and_path(self) -> None:
        scan = scan_workspace(self.root)
        self.assertEqual(match_entities(scan, "alpha")[0].title, "Alpha")
        self.assertEqual(match_entities(scan, str(self.root / "alpha"))[0].id, "alpha")

    def test_malformed_manifest_is_a_visible_diagnostic(self) -> None:
        make_workspace(self.root, malformed=True)
        scan = scan_workspace(self.root)
        self.assertTrue(any(item.code == "manifest-unreadable" for item in scan.diagnostics))

    def test_broken_entity_relationship_is_a_visible_diagnostic(self) -> None:
        make_workspace(self.root, broken=True)
        scan = scan_workspace(self.root)
        self.assertTrue(any(item.code == "unresolved-relationship" for item in scan.diagnostics))

    def test_ambiguous_identifier_returns_four(self) -> None:
        make_workspace(self.root, duplicate=True)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["--workspace-root", str(self.root), "resolve", "alpha"]), 4)

    def test_json_context_has_one_envelope_and_ordered_context(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["--workspace-root", str(self.root), "--json", "context", "alpha"]), 0)
        payload = __import__("json").loads(output.getvalue())
        self.assertEqual(payload["tool"], "wayfinder")
        self.assertEqual(payload["data"]["context"][0]["role"], "workspace-instructions")

    def test_missing_entity_returns_three(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["--workspace-root", str(self.root), "resolve", "missing"]), 3)


if __name__ == "__main__":
    unittest.main()
