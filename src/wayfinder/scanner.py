from __future__ import annotations

import os
import tomllib
from pathlib import Path
from typing import Any, Iterable

from .model import Diagnostic, Entity, ScanResult

EXCLUDED_DIRECTORIES = {
    ".git", ".idea", ".venv", "__pycache__", "node_modules", "build", "dist",
    "target", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox", "City Planning",
    "migration-notes", "templates", "examples", "tests",
}
ENTITY_REFERENCE_RELATIONSHIPS = {
    "depends_on_projects", "used_by_projects", "related_projects", "child_projects", "children",
    "supersedes", "superseded_by",
}


def _windowsish(path: str) -> str:
    candidate = Path(path)
    try:
        if candidate.exists():
            return str(candidate.resolve()).replace("/", "\\").rstrip("\\").casefold()
    except OSError:
        pass
    return path.replace("/", "\\").rstrip("\\").casefold()


def _read_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def _manifest_files(root: Path, recursive: bool) -> Iterable[Path]:
    if not recursive:
        yield from sorted(root.glob("*.manifest.toml"))
        return
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(name for name in dirs if name not in EXCLUDED_DIRECTORIES)
        for name in sorted(files):
            if name.endswith(".manifest.toml"):
                yield Path(current) / name


def _entity_from(path: Path, data: dict[str, Any]) -> Entity:
    def table(name: str) -> dict[str, Any]:
        value = data.get(name, {})
        return value if isinstance(value, dict) else {}

    entity = table("entity")
    project = table("project")
    directory = table("directory")
    lifecycle = table("lifecycle")
    state = table("state")
    paths = table("paths")
    agent = table("agent")
    manifest = table("manifest")
    governance = table("governance")
    relationships = table("relationships")
    read_first = agent.get("read_first", [])
    if not isinstance(read_first, list):
        read_first = []
    declared = paths.get("root") or directory.get("path")
    return Entity(
        id=entity.get("id") or project.get("id"),
        title=entity.get("title") or project.get("title"),
        kind=entity.get("kind") or project.get("type"),
        lifecycle=lifecycle.get("state") or project.get("stage") or state.get("stage"),
        declared_path=declared,
        physical_path=str(path.parent),
        manifest_path=str(path),
        manifest_type=manifest.get("manifest_type"),
        governance=governance,
        relationships=relationships,
        read_first=tuple(item for item in read_first if isinstance(item, str)),
    )


def scan_workspace(workspace_root: Path) -> ScanResult:
    root = workspace_root.resolve()
    workspace_manifest = root / "Development.manifest.toml"
    if not workspace_manifest.is_file():
        raise FileNotFoundError(f"Workspace manifest not found: {workspace_manifest}")
    workspace_data = _read_toml(workspace_manifest)
    diagnostics: list[Diagnostic] = []
    entities: list[Entity] = []
    roots_to_scan: list[tuple[Path, bool]] = [(root, False)]
    deep_kinds = {"portfolio", "intake-incubation", "canonical-standards-root"}
    for registered in workspace_data.get("roots", []):
        if not isinstance(registered, dict) or not isinstance(registered.get("path"), str):
            continue
        registered_path = Path(registered["path"])
        if not registered_path.is_absolute():
            registered_path = root / registered_path
        if registered_path.is_dir():
            roots_to_scan.append((registered_path, registered.get("kind") in deep_kinds))
    seen_manifests: set[Path] = set()
    for scan_root, recursive in roots_to_scan:
        for manifest in _manifest_files(scan_root, recursive):
            manifest = manifest.resolve()
            if manifest in seen_manifests:
                continue
            seen_manifests.add(manifest)
            try:
                data = _read_toml(manifest)
            except (OSError, tomllib.TOMLDecodeError) as exc:
                diagnostics.append(Diagnostic("manifest-unreadable", str(exc), str(manifest)))
                continue
            entities.append(_entity_from(manifest, data))
    entities.sort(key=lambda item: (item.id or "", item.physical_path.casefold(), item.manifest_path.casefold()))
    _append_relationship_diagnostics(entities, diagnostics)
    _append_path_drift_diagnostics(entities, diagnostics)
    return ScanResult(root, workspace_manifest, workspace_data, entities, diagnostics)


def _append_relationship_diagnostics(entities: list[Entity], diagnostics: list[Diagnostic]) -> None:
    ids = {entity.id for entity in entities if entity.id}
    for entity in entities:
        for relationship, value in entity.relationships.items():
            if relationship not in ENTITY_REFERENCE_RELATIONSHIPS or not isinstance(value, list):
                continue
            for item in value:
                if isinstance(item, str) and item and item not in ids:
                    diagnostics.append(Diagnostic(
                        "unresolved-relationship",
                        f"{relationship} references an undiscovered entity: {item}",
                        entity.manifest_path,
                    ))


def _append_path_drift_diagnostics(entities: list[Entity], diagnostics: list[Diagnostic]) -> None:
    for entity in entities:
        if entity.declared_path and entity.declared_path.upper() != "TBD":
            if _windowsish(entity.declared_path) != _windowsish(entity.physical_path):
                diagnostics.append(Diagnostic(
                    "path-drift",
                    "Declared path differs from the manifest's observed directory.",
                    entity.manifest_path,
                ))


def match_entities(scan: ScanResult, identifier: str) -> list[Entity]:
    needle = _windowsish(identifier)
    matches: list[Entity] = []
    for entity in scan.entities:
        candidates = [entity.id, entity.title, entity.declared_path, entity.physical_path]
        if any(value and _windowsish(value) == needle for value in candidates):
            matches.append(entity)
    return matches


def resolve_document(base: Path, declared: str) -> Path:
    candidate = Path(declared)
    return candidate if candidate.is_absolute() else base / candidate
