# The Tier 2 platform

Sources: Proposed Architecture - Knowledge Pipeline Service (6914049, v6); Semantic Knowledge Platform - Cloud + MCP (688162, v7); Qdrant Reference Implementation (6782977, v2); Normalized Knowledge Artifact Contract (2686977, v3); ADR-003 (1048580, v1); ADR-007 (5898241, v1); ADR-008 (8454170, v1). Read the current version of each page before designing; if a page differs from this summary, the page wins.

The platform is **generated per project** in the project's own repository (for example, `<project>-knowledge-platform`), following this architecture. There is no shared platform repository: reusable pieces live in this skill's [assets/platform/](../assets/platform/), and grow only with pieces proven in real projects (ADR-008).

## Architecture

| Decision | Choice |
| --- | --- |
| Style | Hexagonal (ports and adapters) |
| Language | Python for the pipeline service and the Knowledge MCP |
| Ingestion engine | LlamaIndex, only inside outbound adapters |
| Projection | Qdrant (reference default; see [technology.md](technology.md)) |
| AI access | Two MCP servers: **Ops MCP** (operate pipelines) and **Knowledge MCP** (query, read-only) |

| Layer | Contents | May depend on |
| --- | --- | --- |
| Inbound adapters (entry points) | CLI, REST API (webhooks), scheduler, Ops MCP; composition root | Application |
| Application | Use cases | Domain, ports |
| Domain | Contract, entities, value objects, policies | Nothing external |
| Outbound adapters | Source readers, parser and chunker, embedder, vector store, state store, run repository, job queue | Third-party libraries and services |

**Domain model:** `PipelineDefinition` (source, scope, filters, target collection, schedule, exclusions) · `PipelineRun` (mode: full, incremental, single item; trigger; status; timings; counts) · `StepResult` (extract, normalize, parse, chunk, enrich, embed, load, delete, verify) · `RunError` (step, item, version, message, retryable) · `NormalizedKnowledgeArtifact` (contract v2) · policies (exclude the Agent Workspace, validate keys against the key registry, never fabricate fields, report reduced fidelity).

**Use cases:** `RunPipeline` · `HandleSourceEvent` · `RebuildCollection` · `RetryRun` / `CancelRun` · `ListPipelines` / `ListRuns` / `GetRunStatus` · `GetErrors` / `GetReport`.

**Outbound ports:** `SourceReader` (one per provider) · `Parser` / `Chunker` (Docling `HybridChunker`) · `Embedder` (FastEmbed) · `VectorStore` (Qdrant) · `ImageDescriber` (optional, off) · `PipelineDefinitionRepository` (YAML in Git) · `RunRepository` and `StateStore` (SQLite, then PostgreSQL) · `JobQueue` (in-process first).

### Ops MCP

Separate from the Knowledge MCP, so agents that query knowledge cannot trigger rebuilds.

| Tools | Approval |
| --- | --- |
| `list_pipelines`, `list_runs`, `get_run_status`, `get_errors`, `get_report` | Not required |
| `run_incremental`, `retry_run`, `cancel_run` | The agent asks the user to confirm |
| `rebuild_collection` | Explicit approval |

### Knowledge MCP

Read-only: it never runs pipelines and never writes. Tools: `knowledge.search`, `knowledge.get_context`, `knowledge.get_document`, `knowledge.get_decisions`, `knowledge.get_related`, `knowledge.get_gaps`. Every result carries provenance and state; only `validated` knowledge is returned by default; images and diagrams are returned as **links**. `knowledge.propose_change` is **not** part of this service until the proposal flow (Agent Workspace and approval) is designed.

### Webhooks, queue and worker

Verify each webhook's signature or shared secret; debounce bursts per item; handle events idempotently; respond at once and enqueue. Every inbound port only enqueues; the worker executes. One active job per collection; retries with backoff; failed items recorded, never hidden.

### Deployment (docker compose)

`qdrant` · `docling-serve` (if parsing runs as a service) · `pipeline-api` (REST, webhooks, Ops MCP) · `pipeline-worker` · `state-db` (SQLite file first) · `knowledge-mcp`.

## Repository layout

```
<project>-knowledge-platform/
├── pyproject.toml              # uv workspace: members, ruff, pyright, pytest, import-linter
├── uv.lock                     # committed
├── packages/
│   ├── core/src/aief_core/                 # domain + ports + contract; no third-party infrastructure
│   ├── pipeline/src/aief_pipeline/         # application, adapters/, entrypoints/ (composition root)
│   └── knowledge-mcp/src/aief_knowledge_mcp/   # read-only; never imports aief_pipeline
├── pipelines/                  # PipelineDefinition YAML (scope, filters, collection, schedule); no credentials
├── golden-set/                 # questions and expected keys (see verification.md)
├── deploy/compose.yaml
├── .env.example                # variable names only
└── .github/workflows/ci.yml    # uv sync --locked, ruff, pyright, lint-imports, pytest (no network)
```

Three packages because the Knowledge MCP is deployed and secured separately and must not carry the ingestion dependencies. The layer contracts are in [assets/platform/importlinter.toml](../assets/platform/importlinter.toml).

## Toolchain and versions

- **uv** manages Python, the workspace and the lock file; install it only with approval (official installer, user scope). **Docker** runs Qdrant and the services.
- Choose a Python version for which every dependency publishes wheels (Docling usually lags behind the newest Python).
- **Never pin versions from memory.** Let uv resolve current releases and commit `uv.lock`; pin container images to exact tags confirmed in the project's releases; read the current documentation before using an API (for example, `DoclingNodeParser` defaults to `HierarchicalChunker`, so `HybridChunker` must be passed explicitly).
- Check when building: whether the pinned `docling-serve` exposes chunking (if not, the worker runs the Docling library); which Qdrant release supports hybrid queries, sparse IDF and payload indexes.

## Walking skeleton (first increment)

The thinnest slice through every layer, to prove the architecture before anything grows:

```
CLI run <pipeline> --item <page-id>
  → RunPipeline (records a PipelineRun)
  → wiki reader (one page; read-only account from the environment)
  → contract (key, type, state from Page Properties; section from the page tree)
  → Docling: parse and chunk by structure
  → FastEmbed: dense + sparse
  → Qdrant: upsert with deterministic IDs; collection metadata recorded
Knowledge MCP: knowledge.search → chunks with provenance
```

| # | Given | When | Then |
| --- | --- | --- | --- |
| 1 | A page with Page Properties | The pipeline runs | Its chunks carry key, section, type, state and source (provider, ID, URL, version) |
| 2 | The same page, unchanged | It runs again | Same point IDs and count (idempotent) |
| 3 | The collection is deleted | It runs again | The collection and its metadata are reproduced |
| 4 | A page without Page Properties | It runs | `metadata_complete: false`, missing fields listed, state `draft`, no key |
| 5 | The page is indexed | `knowledge.search` with a phrase from the page | The chunk returns with provenance |
| 6 | The repository | CI runs | ruff, pyright, lint-imports and tests pass without network |

Out of the skeleton: attachments, images, labels, incremental runs and deletions, queue, webhooks, scheduler, Ops MCP, the other Knowledge MCP tools, and the work item and board adapters. Each comes in a later increment.

## How to build

- Test first for the domain and the use cases; adapters get contract tests against recorded responses, so CI never calls real services.
- Wiring happens only in the entry points; import-linter fails the build when a layer leaks.
- One pull request per increment, stating what was verified and the resolved versions.
- When the code shows that a framework page is wrong or incomplete, report it and propose the page change.
