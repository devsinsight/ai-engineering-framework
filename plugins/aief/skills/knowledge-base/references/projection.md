# Index and semantic projection

Sources: ADR-007 (5898241, v1), Semantic Knowledge Platform - Cloud + MCP (688162, v3), Normalized Knowledge Artifact Contract (2686977, v2), Building the Knowledge Base (6094849, v2).

## Pipeline shape

```
Sources (wiki · work items · visual board · static files · transcripts)
        ↓  one adapter per source
Normalized Knowledge Artifact (common contract; authority unchanged)
        ↓  processing by type (pages, work items, diagrams, PDF, CSV, transcripts)
Projection
  Tier 1: deterministic index (key, type, title, source/ID/URL/version, state)
  Tier 2: semantic projection (dense + sparse vectors + payload) behind an MCP
        ↓
Consumers: AI agents · deterministic tools · people
```

## Choosing the tier

Start with Tier 1. Move to Tier 2 when any of these holds:

- more than one source, or multimodal content;
- the relevant corpus exceeds what a consumer can read directly;
- permissions differ within the corpus;
- many consumers need centralized audit and token budgeting.

Tier 2 is additive: it reuses the same adapters and normalized artifacts.

## What the MCP must offer (Tier 2)

- **Semantic search** for conceptual questions ("how does payment retry work?").
- **Exact lookup and filters** by key, ID, type or state ("all user stories tagged `feature-checkout-payment`"). Deterministic tools rely on this, not on similarity.
- Results always carry provenance (source, ID, URL, version) and state.
- Consumers never access the vector database directly.

## Pipeline rules

- Preserve provenance and versions; never fabricate a missing field (report reduced fidelity).
- Process incrementally, and **propagate deletions**: an item removed at the source must disappear from the projection.
- The projection must be rebuildable from scratch; deleting it loses nothing.
- Never index secrets; respect source permissions and classification.
- Index transcripts and client documents as Evidence (low authority).
- Exclude the **Agent Workspace** (drafts and reports outside sections 0-8) from indexing (Agent Workflow and Agent Workspace, 6651906, v1).

## Reference defaults and options

Every technology choice is an **option**; the framework names a **reference default** for each one. Recommend the default unless the user has a reason to choose otherwise, and point to the page that lists the alternatives and the criteria.

| Concern | Reference default | Options and criteria |
| --- | --- | --- |
| Metadata from wiki pages | Section from the page tree; key, type and state from Page Properties; labels as traceability; missing fields indexed and flagged | Knowledge Ingestion Pipelines - Guide (6750209, v2), section 5 |
| Chunking | By structure (Docling `HybridChunker`), heading path as context, no overlap | 6750209, v2, section 6 |
| Embeddings | `BAAI/bge-base-en-v1.5` (dense) + `Qdrant/bm25` (sparse), through FastEmbed; the knowledge base is in English | Semantic Search Technology Catalog (6717441, v3), section 4 |
| Reranker | None; add one only when a golden set shows the need | 6717441, v3, sections 5-6 |
| Images | Reference plus deterministic text; the MCP returns the link | 6750209, v2, section 7 |
| Vision model, image repository | Off; none | 6717441, v3, sections 7-8 |
| Visual boards (Miro) | Read by API, one chunk per frame, wiki links become relationships | 6750209, v2, section 8 |
| Projection | Qdrant | 6717441, v3, sections 1-3; Qdrant Reference Implementation (6782977, v2) |
| Pipeline service | Hexagonal Python service; code in `devsinsight/aief-knowledge-platform` | Proposed Architecture - Knowledge Pipeline Service (6914049, v5) |

## Suggested tools (evaluate, not required)

| Need | Examples | Notes |
| --- | --- | --- |
| Unified search over many sources | Onyx (open source); Glean, Atlassian Rovo, Microsoft Copilot connectors (commercial) | Onyx: 40+ connectors, hybrid search, permission sync in its Enterprise license; Azure DevOps connector not confirmed |
| Pipelines into the projection | Airbyte | Confluence source and Qdrant destination with chunking and embeddings; Azure DevOps source not confirmed |
| Semantic database | Qdrant (reference), or any engine with hybrid search and payload filters | Local (for example, docker compose) or cloud |
| Missing connectors | Custom adapters | When a connector does not preserve provenance, versions and permissions |

Claims about tools were reviewed in October 2026; verify before adoption.
