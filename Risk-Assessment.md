# Wayfinder — Risk Assessment

## 1. Metadata Drift and Contradiction

**Risk:** Workspace manifests and documentation may disagree, be incomplete, or evolve across schema generations.

**Impact:** Wayfinder could return misleading results or accidentally conceal governance gaps.

**Control:** Preserve source provenance, report conflicts, and avoid silent reconciliation. A newer or more authoritative source may be identified, but consequential conflicts remain visible.

## 2. Authority Overreach

**Risk:** Context resolution may drift into deciding what should govern rather than reporting what existing governance declares.

**Impact:** Wayfinder could become an undeclared governance authority.

**Control:** Keep core resolution deterministic and rule-based. Separate declared facts, derived links, and diagnostics.

## 3. Scope Expansion

**Risk:** Visualization, repair, indexing, monitoring, AI interpretation, search, and mutation are all attractive adjacent features.

**Impact:** The project could become a large workspace-management platform before the core value is proven.

**Control:** v0.1 remains read-only discovery and context resolution. Adjacent ideas remain evolution findings unless the proposal is deliberately revised.

## 4. Human/Agent Semantic Divergence

**Risk:** Human-readable and machine-readable interfaces could evolve separately and return different interpretations.

**Impact:** Operators and agents could act from inconsistent workspace models.

**Control:** Both output modes consume the same underlying resolution result. Presentation may differ; factual semantics may not.

## 5. Machine Contract Churn

**Risk:** Early output fields, commands, or exit semantics may change before automation consumers can depend on them.

**Impact:** Agent and script integrations become brittle.

**Control:** Use CTS stability levels. Experimental commands may change; stable commands require documented compatibility discipline.

## 6. Performance Pressure Creating Hidden State

**Risk:** Large workspace scans may encourage a persistent index that becomes a second source of truth.

**Impact:** Cache state can drift from authoritative manifests.

**Control:** Any v0.1 cache must be disposable and rebuildable. Cache invalidation or stale-cache behavior must never silently override authoritative source records.

## 7. Security / Trust of Parsed Content

**Risk:** Workspace metadata and referenced files may contain malformed or untrusted content.

**Impact:** Parsing or context assembly could misbehave or accidentally treat content as executable instruction.

**Control:** Treat parsed metadata as data. Reading context does not grant it command authority beyond the workspace governance model already declared by source records.
