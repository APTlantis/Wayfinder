# Wayfinder Command Contract — v0.1.0

## Shared behavior

All commands are stable in v0.1.0. `--workspace-root PATH` selects the inspected workspace and defaults to `D:\`. `--json` writes exactly one CTS JSON envelope to stdout. Normal human-readable data goes to stdout; diagnostics go only to stderr. Wayfinder is read-only.

Stable JSON envelope fields are `status`, `tool`, `version`, and `data`. Entity records use stable `id`, `title`, `kind`, `lifecycle`, `declared_path`, `physical_path`, and `manifest_path` fields. Context entries use `path`, `role`, and `exists`.

## Commands

| Command | Purpose | Stable data |
| --- | --- | --- |
| `wayfinder discover` | List discovered manifest-backed entities. | `workspace_root`, `entities` |
| `wayfinder resolve IDENTIFIER` | Resolve an exact id, title, declared path, or physical path. | `entity` |
| `wayfinder context TARGET` | Emit an ordered declared context bundle. | `entity`, `context` |

The shared options must precede the command: `wayfinder --workspace-root D:\ --json resolve zoning`.

## Exit codes

| Code | Meaning |
| --- | --- |
| `0` | Successful resolution or discovery; warnings may be present. |
| `2` | Invalid command usage. |
| `3` | No supported entity matches the requested identifier. |
| `4` | More than one entity matches the requested identifier. |
| `5` | Workspace root or required workspace manifest could not be read. |

Malformed non-target manifests and broken declared references are reported as diagnostics without manufacturing a result or silently repairing the source.
