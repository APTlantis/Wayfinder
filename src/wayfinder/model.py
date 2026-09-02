from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Diagnostic:
    code: str
    message: str
    path: str | None = None
    severity: str = "warning"

    def to_dict(self) -> dict[str, Any]:
        return {key: value for key, value in asdict(self).items() if value is not None}


@dataclass(frozen=True)
class Entity:
    id: str | None
    title: str | None
    kind: str | None
    lifecycle: str | None
    declared_path: str | None
    physical_path: str
    manifest_path: str
    manifest_type: str | None
    governance: dict[str, Any] = field(default_factory=dict)
    relationships: dict[str, Any] = field(default_factory=dict)
    read_first: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "kind": self.kind,
            "lifecycle": self.lifecycle,
            "declared_path": self.declared_path,
            "physical_path": self.physical_path,
            "manifest_path": self.manifest_path,
            "manifest_type": self.manifest_type,
            "governance": self.governance,
            "relationships": self.relationships,
            "read_first": list(self.read_first),
        }


@dataclass
class ScanResult:
    workspace_root: Path
    workspace_manifest: Path
    workspace_data: dict[str, Any]
    entities: list[Entity]
    diagnostics: list[Diagnostic]
