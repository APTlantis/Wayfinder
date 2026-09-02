# Wayfinder — Success and Completion Criteria

## Project Success Criteria

The project is successful when:

1. Human operators can discover and understand governed workspace entities without reconstructing context manually from scattered files.
2. Agents can obtain the same underlying workspace facts through stable machine-readable output.
3. Supported paths and projects can be resolved to an ordered, source-backed context set.
4. Missing, contradictory, or ambiguous metadata is visible rather than silently normalized.
5. Core operation is local, offline-capable, deterministic, and read-only.
6. WGS and project records remain authoritative; Wayfinder is an operational reader of that truth, not a replacement for it.

## v0.1 Target Shape

**Maturity:** narrow functional command-tool release  
**Completion meaning:** the declared v0.1 workflow is satisfied, not that every useful workspace-intelligence feature exists.

### Required

- Entity discovery.
- Entity lookup.
- Governance/lifecycle/relationship reporting.
- Supported authority/context resolution.
- Ordered context-bundle generation.
- Human-readable output.
- Machine-readable output.
- Explicit error/ambiguity handling.
- Read-only guarantees.
- Representative verification.
- CTS documentation for released commands.

### Expected

- Critical-path verification.
- Operator-minimum documentation.
- Predictable exit behavior.
- Stable fields for commands declared stable.
- Equivalent underlying results across human and machine presentation.

### Optional

- Rebuildable performance cache.
- Additional filters.
- Presentation conveniences.

### Deferred

- GUI and visualization.
- AI/semantic search.
- Repair or mutation.
- Service/API mode.
- Monitoring/watch mode.
- Broad filesystem content search.

## 100% Rule

Wayfinder v0.1 is 100% complete when its declared required scope and expected maturity are satisfied with valid evidence and no blockers.

Newly discovered enhancements are evolution findings. They do not reduce completion unless they reveal a defect, contradiction, missing declared requirement, safety issue, or invalid verification evidence.
