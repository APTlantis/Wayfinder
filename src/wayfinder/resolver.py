from __future__ import annotations

from pathlib import Path
from typing import Any

from .model import Diagnostic, Entity, ScanResult
from .scanner import resolve_document


def context_for(scan: ScanResult, entity: Entity) -> dict[str, Any]:
    diagnostics: list[Diagnostic] = []
    entries: list[dict[str, str]] = []
    seen: set[str] = set()

    def add(path: Path, role: str, required: bool = False) -> None:
        key = str(path).casefold()
        if key in seen:
            return
        seen.add(key)
        exists = path.is_file()
        entries.append({"path": str(path), "role": role, "exists": str(exists).lower()})
        if not exists:
            diagnostics.append(Diagnostic("missing-context-record", f"Declared {role} record is missing.", str(path), "error" if required else "warning"))

    root = scan.workspace_root
    add(root / "AGENTS.md", "workspace-instructions", required=True)
    add(scan.workspace_manifest, "workspace-manifest", required=True)

    target_dir = Path(entity.physical_path)
    ancestors = list(reversed([path for path in [target_dir, *target_dir.parents] if path != root and root in [path, *path.parents]]))
    for directory in ancestors:
        add(directory / "AGENTS.md", "inherited-instructions")
        manifests = sorted(directory.glob("*.manifest.toml"))
        for manifest in manifests:
            if str(manifest) != entity.manifest_path:
                add(manifest, "directory-manifest")

    add(Path(entity.manifest_path), "target-manifest", required=True)
    manifest_dir = Path(entity.manifest_path).parent
    for declared in entity.read_first:
        add(resolve_document(manifest_dir, declared), "declared-read-first")

    standards = scan.workspace_data.get("standards", {})
    governance = entity.governance
    names = [governance.get("primary_standard"), governance.get("release_standard"), *governance.get("additional_standards", [])]
    for name in names:
        if isinstance(name, str) and name and name.casefold() in standards:
            add(Path(standards[name.casefold()]) / "README.md", "governing-standard")

    return {
        "entity": entity.to_dict(),
        "context": entries,
        "diagnostics": [item.to_dict() for item in diagnostics],
    }
