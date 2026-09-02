# Wayfinder — Scope Boundary

## Governing Intent

Wayfinder operationalizes the workspace metadata spine without becoming a second governance authority.

Its boundary is simple:

> Read, resolve, explain, and assemble context. Do not mutate workspace truth.

## In Scope

- Local discovery of governed workspace entities.
- Deterministic lookup by supported identifiers and paths.
- Reporting declared identity, lifecycle, governance, relationships, and read-first context.
- Authority/context-chain resolution based on existing governance records.
- Ordered context bundles for humans and agents.
- Human-readable and machine-readable command output.
- Explicit provenance and ambiguity reporting.

## Non-Goals

Wayfinder is not:

- A manifest editor.
- A workspace migrator.
- A project generator.
- A governance decision engine.
- A lifecycle controller.
- A policy enforcement service.
- A filesystem indexing replacement.
- A semantic search engine.
- An AI agent.
- A dashboard.
- A background watcher.
- A network service.

## Trust Boundary

Authoritative truth remains in WGS-governed manifests, AGENTS.md files, indexes, project documentation, and governing standards.

Wayfinder may report:

- declared facts;
- resolved relationships derived mechanically from declared facts;
- diagnostics about missing, contradictory, or broken metadata.

It must not present an unsupported inference as authoritative workspace truth.

## Proposal-Revision Triggers

A PPS revision is required before Wayfinder:

- mutates authoritative workspace state;
- automatically repairs manifests;
- makes governance or lifecycle decisions;
- introduces probabilistic/AI interpretation into core resolution;
- becomes a continuously running service;
- adopts a second authoritative metadata store;
- changes from equal human/agent support to privileging one as the defining purpose.
