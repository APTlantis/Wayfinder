# Wayfinder — Project Proposal

## Project Identity

**Project Name:** Wayfinder  
**Project Class:** Command Tool  
**WGS Lifecycle State:** planning  
**PPS Readiness:** ready  
**Primary Governing Standard:** PPS  
**Delivery Standard:** CTS  
**Project Theme:** Deterministic workspace discovery and context resolution for humans and agents.

## Problem Statement

The Aptlantis development workspace increasingly describes itself through entity manifests, directory manifests, project manifests, standards, AGENTS.md files, read-first guidance, lifecycle metadata, relationships, and root-level indexes.

That information is intentionally durable and machine-readable, but using it still requires a human or agent to know where to look, traverse multiple files, interpret relationships, and reconstruct which documents are authoritative for a project or path.

Human operators experience this as navigation and context-recovery friction. Agents experience the same underlying problem as context-assembly and authority-resolution friction.

Today the problem is solved manually: begin from an index or known project path, inspect manifests and AGENTS.md files, follow relationships, identify governing standards, and assemble the relevant context. This works, but it does not operationalize the metadata layer as a queryable workspace system.

## Mission Statement

Wayfinder is a local, read-only workspace query and context-resolution tool that allows human operators and agents, as equal first-class users, to discover governed entities, resolve relationships and authority, and assemble the relevant read-first context from the Aptlantis metadata spine without altering workspace state.

## Intended Users and Operators

### Human Operator
Uses Wayfinder to locate projects, standards, datasets, services, and other governed entities; inspect lifecycle and relationship information; determine what governs a path or project; and recover context without manually traversing the workspace.

### Agent
Uses Wayfinder through stable machine-readable command output to identify authoritative context, determine governing relationships, and assemble an ordered context set before acting on a workspace entity.

Neither persona is secondary. A successful design must support both from the same underlying deterministic workspace model.

## Design Boundaries

### In Scope

Wayfinder will:

- Discover governed entities from the existing workspace metadata spine.
- Read WGS-style entity manifests and relevant root/directory/project metadata.
- Resolve an entity from a name, id, known path, or other supported deterministic identifier.
- Surface lifecycle state, project class, governing standards, relationships, and documented read-first material.
- Resolve the applicable authority/context chain for a supported project or path.
- Assemble an ordered context bundle suitable for a human or an agent to read.
- Provide human-readable CLI output.
- Provide explicit machine-readable output suitable for automation and agent use.
- Operate locally and remain useful offline.
- Report ambiguity, missing metadata, broken relationships, or unsupported cases rather than silently guessing.

### Out of Scope

Wayfinder v0.1 does not:

- Modify, repair, migrate, normalize, or generate authoritative workspace manifests.
- Move, rename, create, archive, activate, or otherwise mutate projects or workspace entities.
- Decide lifecycle state, project status, governance policy, or authority on its own.
- Replace WGS, PPS, project manifests, AGENTS.md, INDEX.md, or other authoritative source documents.
- Become a general filesystem search engine or content search replacement.
- Perform semantic/vector search.
- Require an LLM or AI model for its core function.
- Provide a GUI, dashboard, HTTP service, daemon, or background monitor.
- Continuously index or watch the workspace.
- Treat inferred relationships as authoritative facts.

### Change-Control Boundary

Adding mutation, autonomous governance decisions, semantic/AI interpretation, continuous monitoring, or a persistent service changes the nature or trust posture of the project and requires an explicit PPS revision rather than ordinary feature growth.

## Success Criteria

Wayfinder is successful for its first version when:

1. A human can identify a governed entity and obtain its key identity, lifecycle, governance, relationship, and read-first information without manually locating each source document.
2. An agent can request equivalent information in documented machine-readable form and reliably distinguish data from diagnostics.
3. Given a supported project or path, Wayfinder can produce an ordered context set identifying the relevant authoritative and read-first documents used to orient before modification.
4. Wayfinder reports unresolved ambiguity, missing manifests, broken references, and unsupported cases explicitly instead of manufacturing certainty.
5. The tool remains read-only: normal operation does not mutate authoritative workspace state.
6. Equivalent inputs resolve deterministically against an unchanged workspace state.
7. The command surface is documented well enough that both a human and automation consumer can use it without reading implementation source.

## Failure Criteria

The project has failed or requires redesign if:

- Core workspace discovery depends on cloud access or an external hosted service.
- AI or probabilistic interpretation becomes necessary for basic identity, authority, relationship, or context resolution.
- Wayfinder silently creates or overrides authoritative workspace truth.
- Human output and machine output are backed by materially different resolution logic.
- Agents cannot reliably distinguish confirmed metadata from ambiguity, missing data, or diagnostics.
- The tool becomes a workspace mutation or governance-enforcement engine without a deliberate proposal revision.
- Maintaining a second proprietary metadata store becomes necessary to know facts already represented authoritatively in the workspace.

## Technical Direction

Technical direction is intentionally limited at proposal stage.

- **Primary delivery shape:** Local command-line tool.
- **Primary runtime:** Local Windows development workspace.
- **Primary data source:** Existing Aptlantis/WGS manifests and documented workspace metadata.
- **Primary behavior:** Read-only discovery, resolution, querying, and context assembly.
- **Human interface:** Text-first CLI.
- **Automation interface:** Explicit machine-readable output, expected to use JSON under CTS conventions.
- **Language/framework:** TBD during implementation design; no language choice is required by the present mission.
- **Persistent storage:** Not required for v0.1. An implementation may use ephemeral or rebuildable acceleration only if authoritative truth remains in workspace source records.
- **Network dependency:** None required for core operation.

## Constraints

- Must work offline for its core function.
- Must remain local-first.
- Must remain read-only for v0.1.
- Must not require accounts.
- Must not require AI or an LLM.
- Must preserve WGS and project documents as the sources of authority.
- Must surface uncertainty rather than hide it.
- Must support both human and agent consumers as first-class users.
- Must provide deterministic behavior for unchanged inputs and workspace state.
- Must remain understandable and operable by a single maintainer.
- Machine-readable behavior must conform to the applicable CTS command contract.

## Dependencies

### Required

- Existing Aptlantis workspace metadata and WGS entity-manifest conventions.
- Stable enough manifest parsing to identify entity, governance, lifecycle, relationship, path, documentation, and agent/read-first fields where present.
- CTS for public command/output behavior.

### Contextual

- Root and directory indexes such as INDEX.md.
- AGENTS.md files and manifest-declared read-first/authoritative documents.
- PPS, WGS, and domain-standard metadata referenced by projects.

### Not Required

- Network access.
- Cloud services.
- AI/LLM services.
- A database server.
- A long-running service.

## Major Risks

1. **Metadata inconsistency or drift.** Real workspace records may be incomplete, contradictory, stale, or differently shaped.
   - Mitigation: preserve provenance, expose ambiguity, and avoid silent reconciliation.

2. **Authority overreach.** A query tool could accidentally begin deciding what is authoritative instead of reporting what governance records declare.
   - Mitigation: keep resolution rule-based and source-backed; distinguish declared facts from tool diagnostics.

3. **Scope growth into a workspace platform.** Search, repair, monitoring, visualization, AI interpretation, and mutation are all plausible adjacent capabilities.
   - Mitigation: keep v0.1 to read-only discovery and context resolution; treat adjacent capabilities as evolution findings unless deliberately promoted.

4. **Human/agent divergence.** Separate code paths could produce different truths for different consumers.
   - Mitigation: both output modes must derive from the same resolution model.

5. **Unstable machine contract.** Agent usefulness can be undermined if fields, exit codes, or semantics churn casually.
   - Mitigation: apply CTS stability levels and only call automation-facing commands stable once their contract is documented and verified.

## Roadmap

### Phase 1 — Metadata Spine
Establish the supported source records and deterministic internal representation needed to discover entities and preserve provenance.

### Phase 2 — Core Resolution Workflows
Implement the minimum discovery, lookup, relationship, authority, and context-assembly workflows needed to prove both human and agent use cases.

### Phase 3 — Verification
Verify deterministic behavior, ambiguity handling, broken-reference behavior, read-only guarantees, representative workspace examples, and human/machine equivalence.

### Phase 4 — CTS Release Readiness
Document command contracts, exit codes, structured-output shapes, help/version behavior, examples, and release evidence required for a CTS-governed command tool.

## v0.1 Completion Boundary

Wayfinder v0.1 is a narrow but complete vertical slice of workspace intelligence.

### Required

- Governed entity discovery from supported workspace manifests.
- Deterministic entity lookup.
- Relationship and governance reporting from declared metadata.
- Path/project context resolution for supported cases.
- Ordered context-bundle output.
- Human-readable CLI output.
- Explicit machine-readable output.
- Clear ambiguity and failure reporting.
- Read-only operation.
- CTS command documentation sufficient for the released surface.
- Verification against representative real workspace entities.

### Expected at This Maturity

- Basic but reliable error handling.
- Critical-path tests or equivalent executable verification.
- Operator-minimum documentation.
- Stable-enough JSON fields for the commands explicitly declared stable.
- Evidence that human and agent outputs use the same underlying resolution results.

### Optional

- Rebuildable local cache or generated index for speed.
- Convenience filtering and presentation features that do not alter the core model.
- Additional query predicates beyond those necessary for the v0.1 success criteria.

### Deliberately Deferred

- GUI.
- Relationship visualization.
- Semantic or vector search.
- AI interpretation.
- Automatic metadata repair.
- Workspace mutation.
- Continuous monitoring or file watching.
- HTTP/API service.
- Background daemon.
- General-purpose full-text file search.
- Policy enforcement.

### Completion Evidence

v0.1 may be assessed as 100% complete when all required items are demonstrated, expected maturity items are satisfied at the declared level, no completion blocker remains, and the release evidence required by CTS is present.

Additional useful ideas discovered after that point are evolution findings and do not reduce v0.1 completion unless they expose a missing declared requirement, defect, contradiction, safety problem, or invalid evidence.

## Governance Handoff

This proposal is `ready`.

Broad implementation may begin within this boundary. WGS owns workspace placement and registration. CTS governs the released command surface. Any future library surface may be evaluated separately for LDS applicability if it becomes an independently consumed library rather than merely internal implementation.
