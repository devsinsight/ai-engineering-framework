# Architecture of the knowledge platform

Sources: Proposed Architecture - Knowledge Pipeline Service (6914049, v5); Semantic Knowledge Platform - Cloud + MCP (688162, v6); Qdrant Reference Implementation (6782977, v2); Normalized Knowledge Artifact Contract (2686977, v3); ADR-003 (1048580, v1); ADR-007 (5898241, v1). This file summarizes them; if a page has a newer version, the page wins.

## Pages to read before designing

| Page | Why |
| --- | --- |
| Proposed Architecture - Knowledge Pipeline Service (6914049) | Layers, domain model, use cases, ports, stores, deployment |
| Knowledge Ingestion Pipelines - Guide (6750209) | Reference pipeline, metadata, chunking, images, Miro |
| Normalized Knowledge Artifact Contract (2686977) | The data every adapter must produce |
| Qdrant Reference Implementation (6782977) | Collection design, payload, indexes, query patterns |
| Semantic Knowledge Platform - Cloud + MCP (688162) | Knowledge MCP tools, ingestion and retrieval flows, security |
| Semantic Search Technology Catalog (6717441) | Options and criteria for embeddings, rerankers, vision, image repositories |
| AI Tooling for the Knowledge Base (6488066), section 7 | Least-privilege accounts for every integration |

## Style and decisions

| Decision | Choice |
| --- | --- |
| Architectural style | Hexagonal (ports and adapters) |
| Language | Python for the pipeline service and the Knowledge MCP |
| Ingestion engine | LlamaIndex, contained in the outbound adapters |
| Projection | Qdrant (reference default) |
| AI access | Two MCP servers: **Ops MCP** (operate pipelines) and **Knowledge MCP** (query knowledge, read-only) |

## Layers

| Layer | Contents | May depend on |
| --- | --- | --- |
| Inbound adapters (entry points) | CLI, REST API (webhooks, triggers), scheduler, Ops MCP; a web UI later | Application |
| Application | Use cases: orchestrate, record every run, apply policies, enqueue jobs | Domain, outbound ports |
| Domain | Entities, value objects, policies | Nothing external |
| Outbound adapters | Source readers, parser, chunker, embedder, vector store, state store, run repository, job queue | Third-party libraries and services |

## Domain model

| Element | Meaning |
| --- | --- |
| `PipelineDefinition` | Source, scope (space, project, board), filters, target collection, schedule, exclusions |
| `PipelineRun` | One execution: mode (full, incremental, single item), trigger (webhook, command, schedule, agent), status, timings, counts |
| `StepResult` | Outcome of each step: extract, normalize, parse, chunk, enrich, embed, load, delete, verify |
| `RunError` | Step, item (source, ID, version), message, retryable or not |
| `NormalizedKnowledgeArtifact` | The framework contract (schema version 2) |
| Policies | Exclude the Agent Workspace; validate keys against the key registry; never fabricate missing fields; report reduced fidelity |

## Use cases

`RunPipeline` (full, incremental, single item) · `HandleSourceEvent` (webhook → incremental run) · `RebuildCollection` · `RetryRun` / `CancelRun` · `ListPipelines` / `ListRuns` / `GetRunStatus` · `GetErrors` / `GetReport` (freshness, counts, failures).

## Outbound ports

| Port | Reference adapter |
| --- | --- |
| `SourceReader` (one per provider) | Confluence (LlamaIndex reader or REST), Azure DevOps (REST: WIQL then batch), Miro (REST API v2) |
| `Parser` / `Chunker` | Docling, chunking by structure with `HybridChunker` |
| `Embedder` | FastEmbed: `BAAI/bge-base-en-v1.5` (dense) + `Qdrant/bm25` (sparse) |
| `VectorStore` | Qdrant (hybrid: named dense and sparse vectors, payload indexes) |
| `ImageDescriber` (optional, off) | Docling picture description |
| `PipelineDefinitionRepository` | YAML files versioned in Git |
| `RunRepository` | SQLite, then PostgreSQL |
| `StateStore` | Per-document hashes for incremental runs and deletions, on the same database |
| `JobQueue` | In-process first; a dedicated queue when load requires it |

## Inbound ports

### Ops MCP

Separate from the Knowledge MCP, so agents that query knowledge cannot trigger rebuilds (least privilege).

| Tools | Type | Approval |
| --- | --- | --- |
| `list_pipelines`, `list_runs`, `get_run_status`, `get_errors`, `get_report` | Read | Not required |
| `run_incremental`, `retry_run`, `cancel_run` | Action | The agent asks the user to confirm |
| `rebuild_collection` | Destructive | Explicit approval |

### REST API (webhooks)

Verify each webhook's signature or shared secret; debounce bursts per item; make handling idempotent; respond immediately and enqueue the job, never run the pipeline inside the request.

### CLI and scheduler

The CLI runs the same use cases from a terminal. The scheduler triggers periodic incremental runs and occasional full rebuilds.

## Job queue and worker

Every inbound port only enqueues jobs; the worker executes them. One active job per collection; retries with backoff for transient errors; failed items are recorded, never hidden.

## Knowledge MCP

A separate, read-only service. It never runs pipelines and never writes to sources. Tools:

```
knowledge.search(query, filters)
knowledge.get_context(topic, scope)
knowledge.get_document(key_or_document_id)
knowledge.get_decisions(topic)
knowledge.get_related(key_or_topic)
knowledge.get_gaps(topic)
```

Every result carries provenance (source, ID, URL, version) and state. Only `validated` knowledge is returned by default. For images and diagrams it returns the **link** to the original, never binaries. `knowledge.propose_change` is part of the framework's contract but writes proposals, so it is out of the read-only service until the approval flow is designed.

## Deployment (docker compose)

| Service | Role |
| --- | --- |
| `qdrant` | Semantic projection |
| `docling-serve` | Document parsing (REST API) |
| `pipeline-api` | REST API, webhooks and Ops MCP |
| `pipeline-worker` | Executes jobs |
| `state-db` | Runs, errors and document hashes (SQLite file first, PostgreSQL later) |
| `knowledge-mcp` | Read-only Knowledge MCP |

## Cross-cutting rules

- **Security:** least-privilege, read-only source accounts; secrets in environment variables or a secret manager; vector database keys never exposed to AI clients.
- **Observability:** structured logs per run and step; counts and durations; errors linked to the exact item and version.
- **Rebuildability:** deterministic point IDs and content hashes; a full rebuild reproduces the projection.
- **Provenance:** every chunk keeps the contract fields.
