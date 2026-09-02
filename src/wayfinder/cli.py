from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from . import __version__
from .model import Diagnostic, Entity, ScanResult
from .resolver import context_for
from .scanner import match_entities, scan_workspace

TOOL = "wayfinder"


def _envelope(status: str, data: dict[str, Any], diagnostics: list[Diagnostic] | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"status": status, "tool": TOOL, "version": __version__, "data": data}
    if diagnostics:
        result["warnings" if status != "error" else "errors"] = [item.to_dict() for item in diagnostics]
    return result


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=TOOL, description="Read-only Aptlantis workspace discovery and context resolution.")
    parser.add_argument("--version", action="version", version=f"{TOOL} {__version__}")
    parser.add_argument("--workspace-root", type=Path, default=Path("D:\\"), help="Workspace root (default: D:\\).")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit one CTS JSON envelope on stdout.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("discover", help="List manifest-backed workspace entities.")
    resolve = subparsers.add_parser("resolve", help="Resolve one exact entity identifier.")
    resolve.add_argument("identifier")
    context = subparsers.add_parser("context", help="Assemble declared orientation context for one entity.")
    context.add_argument("target")
    return parser


def _text_discover(scan: ScanResult) -> str:
    lines = ["ID\tTITLE\tKIND\tLIFECYCLE\tPHYSICAL PATH"]
    lines.extend(f"{item.id or '-'}\t{item.title or '-'}\t{item.kind or '-'}\t{item.lifecycle or '-'}\t{item.physical_path}" for item in scan.entities)
    return "\n".join(lines)


def _emit(args: argparse.Namespace, status: str, data: dict[str, Any], diagnostics: list[Diagnostic], text: str) -> int:
    if args.json_output:
        print(json.dumps(_envelope(status, data, diagnostics), indent=2, sort_keys=True))
    else:
        print(text)
    for diagnostic in diagnostics:
        print(f"{diagnostic.severity}: {diagnostic.code}: {diagnostic.message}" + (f" ({diagnostic.path})" if diagnostic.path else ""), file=sys.stderr)
    return 0


def _run(argv: list[str] | None = None) -> int:
    parser = _parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code)
    try:
        scan = scan_workspace(args.workspace_root)
    except (FileNotFoundError, OSError, ValueError) as exc:
        diagnostic = Diagnostic("workspace-unreadable", str(exc), str(args.workspace_root), "error")
        if args.json_output:
            print(json.dumps(_envelope("error", {}, [diagnostic]), indent=2, sort_keys=True))
        else:
            print(f"error: {diagnostic.message}", file=sys.stderr)
        return 5
    if args.command == "discover":
        data = {"workspace_root": str(scan.workspace_root), "entities": [entity.to_dict() for entity in scan.entities]}
        return _emit(args, "warning" if scan.diagnostics else "ok", data, scan.diagnostics, _text_discover(scan))
    identifier = args.identifier if args.command == "resolve" else args.target
    matches = match_entities(scan, identifier)
    if not matches:
        diagnostic = Diagnostic("not-found", f"No entity matches: {identifier}", severity="error")
        if args.json_output:
            print(json.dumps(_envelope("error", {}, [diagnostic]), indent=2, sort_keys=True))
        else:
            print(f"error: {diagnostic.message}", file=sys.stderr)
        return 3
    if len(matches) > 1:
        diagnostic = Diagnostic("ambiguous-identifier", f"Multiple entities match: {identifier}", severity="error")
        data = {"matches": [item.to_dict() for item in matches]}
        if args.json_output:
            print(json.dumps(_envelope("error", data, [diagnostic]), indent=2, sort_keys=True))
        else:
            print("error: " + diagnostic.message, file=sys.stderr)
            print("\n".join(item.manifest_path for item in matches), file=sys.stderr)
        return 4
    entity = matches[0]
    if args.command == "resolve":
        return _emit(args, "warning" if scan.diagnostics else "ok", {"entity": entity.to_dict()}, scan.diagnostics, json.dumps(entity.to_dict(), indent=2))
    result = context_for(scan, entity)
    diagnostics = scan.diagnostics + [Diagnostic(**item) for item in result.pop("diagnostics")]
    text = "\n".join(f"{item['role']}: {item['path']}" for item in result["context"])
    return _emit(args, "warning" if diagnostics else "ok", result, diagnostics, text)


def main(argv: list[str] | None = None) -> int:
    try:
        return _run(argv)
    except Exception as exc:  # Defensive boundary for the stable CLI contract.
        diagnostic = Diagnostic("internal-error", str(exc), severity="error")
        arguments = argv if argv is not None else sys.argv[1:]
        if "--json" in arguments:
            print(json.dumps(_envelope("error", {}, [diagnostic]), indent=2, sort_keys=True))
        else:
            print(f"error: {diagnostic.message}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
