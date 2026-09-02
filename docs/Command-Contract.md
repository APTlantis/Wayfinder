# Wayfinder Command Contract — v0.1.0

## Purpose

Wayfinder reads Aptlantis workspace metadata and reports deterministic entity discovery, exact entity resolution, and declared orientation context. It never modifies the inspected workspace.

## Usage

```text
wayfinder [--workspace-root PATH] [--json | --markdown] discover [--include-incomplete] [--diagnostics]
wayfinder [--workspace-root PATH] [--json | --markdown] resolve IDENTIFIER
wayfinder [--workspace-root PATH] [--json | --markdown] context TARGET
```

## Inputs

- Arguments: `IDENTIFIER` and `TARGET` are exact entity id, title, declared path, or observed physical path values.
- Options: `--workspace-root PATH` defaults to `D:\`; `--json` requests machine output; `--markdown` emits a copy-pasteable Markdown table. `discover --include-incomplete` exposes template/incomplete records; `discover --diagnostics` emits workspace-wide diagnostics.
- Environment: none.
- Files: `Development.manifest.toml`, registered root manifests, declared read-first files, and governing standard READMEs. Parsed content is never executed.

## Outputs

### Human Output

`discover` writes a curated tabular entity list to stdout, including only records with an id, title, and kind. `--include-incomplete` exposes raw records. `resolve` writes the resolved entity record. `context` writes ordered `role: path` context entries. `--markdown` renders each result as a Markdown table. Normal warnings and errors are not mixed into stdout.

### Machine Output

With `--json`, stdout contains exactly one CTS envelope. Stable top-level fields are `status`, `tool`, `version`, and `data`; warnings or errors are structured arrays. Stable entity fields are `id`, `title`, `kind`, `lifecycle`, `declared_path`, `physical_path`, and `manifest_path`. Stable context fields are `path`, `role`, and `exists`.

### Diagnostics

`discover` reports workspace-wide parse observations, unresolved entity relationships, and path drift. `resolve` and `context` report only diagnostics sourced by the selected entity plus missing records in that entity's context bundle. All diagnostics and errors go to stderr; JSON-mode stdout contains no progress or diagnostic text.

## Exit Codes

| Code | Meaning |
| --- | --- |
| 0 | Successful discovery or resolution; warnings may be present. |
| 1 | Unexpected internal failure. |
| 2 | Invalid command usage. |
| 3 | No supported entity matches the requested identifier. |
| 4 | More than one entity matches the requested identifier. |
| 5 | Workspace root or required workspace manifest could not be read. |

## Stability

- Command name: `discover`, `resolve`, and `context` are stable in v0.1.0.
- Flag names: `--workspace-root`, `--json`, `--markdown`, `--include-incomplete`, and `--diagnostics` are stable.
- Machine-readable fields: fields documented in Machine Output are stable for automation.
- Breaking-change policy: removing or changing stable commands, flags, exit-code meanings, stdout/stderr behavior, or stable field types requires a major-version migration note.

## Examples

### Human Use

```text
wayfinder --workspace-root D:\ discover
wayfinder resolve zoning
wayfinder context D:\.zoning\Wayfinder
wayfinder --markdown discover
```

### Automation Use

```text
wayfinder --workspace-root D:\ --json resolve zoning
wayfinder --json context D:\.zoning\Wayfinder
```
