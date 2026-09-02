# Wayfinder

Wayfinder is a local, read-only command-line tool for discovering Aptlantis workspace entities and recovering their declared operating context. It gives people and agents the same deterministic view of manifests, instructions, lifecycle records, relationships, and governing standards—without changing workspace state.

## What it does

- Lists current manifest-backed workspace entities.
- Resolves an entity by exact id, title, declared path, or observed path.
- Builds an ordered context bundle for a project, directory, or workspace entity.
- Emits human-readable text or a stable CTS JSON envelope.
- Reports metadata drift and broken declared relationships explicitly when asked to audit them.

Wayfinder does not edit manifests, move files, execute workspace content, maintain a cache, contact the network, run a service, or watch the filesystem.

## Install and run

From this directory, install the local editable package:

```powershell
python -m pip install -e .
```

The default workspace root is `D:\`. Override it for another workspace or an isolated test fixture with `--workspace-root PATH`.

```powershell
# Curated current entity list: complete records only, no global diagnostics.
wayfinder discover

# Resolve a known entity.
wayfinder resolve wayfinder

# Recover the authority and read-first context for an entity.
wayfinder context zoning

# Inspect another workspace root explicitly.
wayfinder --workspace-root D:\.zoning\Wayfinder context wayfinder
```

## Discovery and audit views

`discover` is intentionally calm by default: it shows entities with a declared id, title, and kind, and does not append workspace-wide diagnostics.

Use the audit switches when you need the raw intake picture:

```powershell
# Include incomplete/template-like records.
wayfinder discover --include-incomplete

# Include workspace-wide path-drift, parse, and relationship diagnostics.
wayfinder discover --diagnostics

# Full raw discovery audit.
wayfinder discover --include-incomplete --diagnostics
```

`resolve` and `context` only report diagnostics attached to the selected entity or its context bundle, so a useful lookup is not drowned out by unrelated historical drift.

## Automation and JSON

Put global options before the command. In JSON mode, stdout contains exactly one CTS envelope; diagnostics stay on stderr.

```powershell
wayfinder --json resolve wayfinder
wayfinder --workspace-root D:\ --json context zoning
```

Stable JSON envelope fields are `status`, `tool`, `version`, and `data`. See the [command contract](docs/Command-Contract.md) and [JSON examples](docs/JSON-Examples.md) for the stable entity and context fields, diagnostics, and exit codes.

## Development

The dependency-free Python package lives in `src\wayfinder`; tests use isolated temporary workspace fixtures.

```powershell
python -m unittest discover -s tests -v
```

The project is intentionally retained in `D:\.zoning` while its v0.1 command surface is reviewed. Local tests validate the implementation, not package publication, signing, hashing, or release readiness.

## Governance and project records

- [Project overview and handoff](Project-README.md)
- [Project proposal](Project-Proposal.md)
- [Scope boundary](Scope-Boundary.md)
- [Command contract](docs/Command-Contract.md)
- [Architecture](docs/Architecture.md)
- [Project manifest](Wayfinder.manifest.toml)
