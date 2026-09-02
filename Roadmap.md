# Wayfinder — Roadmap

## Phase 1: Metadata Spine

Purpose: establish the minimum deterministic model Wayfinder needs to understand governed workspace entities.

Completion shape:

- Supported manifest/document sources are identified.
- Provenance is retained.
- Entity identity and relationship fields can be represented without inventing missing values.
- Ambiguity and malformed-source behavior are defined.

## Phase 2: Core Workflows

Purpose: prove Wayfinder's mission for both first-class personas.

Completion shape:

- Human operator can discover and inspect a governed entity.
- Agent can request equivalent machine-readable facts.
- Supported path/project can resolve to governance and read-first context.
- Ordered context bundle can be emitted.
- No workflow mutates authoritative workspace state.

## Phase 3: Verification

Purpose: establish that the result is dependable enough to use for workspace orientation.

Completion shape:

- Representative real entities are exercised.
- Broken links, missing manifests, and contradictory metadata are tested.
- Same workspace state produces deterministic results.
- Human and machine outputs are shown to derive from the same resolution model.
- Read-only behavior is verified.

## Phase 4: CTS Release Readiness

Purpose: turn the working vertical slice into a governed command-tool release.

Completion shape:

- Command contracts are documented.
- Exit codes are documented and verified.
- Human stdout/stderr behavior is correct.
- Machine-readable output is parseable and free of progress noise.
- Help, version, examples, and error examples exist.
- Released commands have explicit stability levels.
