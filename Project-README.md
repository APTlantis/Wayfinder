# Wayfinder

## Purpose and boundary

Wayfinder is a local Python CLI that discovers Aptlantis manifest-backed entities and assembles declared, source-backed workspace context for people and agents. v0.1 is deterministic, offline-capable, and strictly read-only.

## Governance

- Project record: [Wayfinder.manifest.toml](Wayfinder.manifest.toml)
- Project proposal: [Project-Proposal.md](Project-Proposal.md)
- Command contract: [docs/Command-Contract.md](docs/Command-Contract.md)
- Read map: [PROJECT-READMAP.toml](PROJECT-READMAP.toml)
- Governing standards: WGS, PPS, and CTS under `D:\.city_hall`.

## Commands

`wayfinder discover`, `wayfinder resolve IDENTIFIER`, and `wayfinder context TARGET` all accept `--workspace-root`; it defaults to `D:\`. Add `--json` for the CTS JSON envelope.

The source package is under `src\wayfinder`; tests use isolated fixture workspaces under `tests`. Wayfinder maintains no index, cache, service, network connection, or persistent state.

## Current state

v0.1 has a local implementation and executable verification. It is retained in zoning while its command surface is reviewed; this is not CTS promotion, package publication, or release evidence.
