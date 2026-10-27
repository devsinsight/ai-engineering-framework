# Repository layout

Decided with the framework owner (2026-10-27): a **uv workspace with three packages**, MIT license, hexagonal layers enforced by import-linter. The architecture it implements is in [architecture.md](architecture.md).

## Tree

```
aief-knowledge-platform/
├── pyproject.toml                  # workspace root: members, dev tools, ruff, pyright, pytest, import-linter
├── uv.lock                         # pinned versions (committed)
├── packages/
│   ├── core/                       # aief_core: domain + ports + contract; no third-party infrastructure
│   │   ├── pyproject.toml
│   │   ├── src/aief_core/
│   │   │   ├── domain/             # artifact (contract v2), chunk, pipeline, run, policies, ids
│   │   │   └── ports/              # SourceReader, Chunker, Embedder, VectorStore, RunRepository, StateStore, ...
│   │   └── tests/
│   ├── pipeline/                   # aief_pipeline: use cases + outbound adapters + entry points
│   │   ├── pyproject.toml
│   │   ├── src/aief_pipeline/
│   │   │   ├── application/        # use cases (RunPipeline, RebuildCollection, ...)
│   │   │   ├── adapters/
│   │   │   │   ├── sources/        # confluence, azure_devops, miro
│   │   │   │   ├── parsing/        # docling
│   │   │   │   ├── embedding/      # fastembed
│   │   │   │   ├── projection/     # qdrant
│   │   │   │   ├── persistence/    # run repository, state store, definition repository
│   │   │   │   └── queue/
│   │   │   └── entrypoints/        # cli, api (webhooks), worker, scheduler, ops_mcp; composition root
│   │   └── tests/                  # unit, contract (recorded responses), e2e (marked, opt-in)
│   └── knowledge-mcp/              # aief_knowledge_mcp: read-only query service
│       ├── pyproject.toml          # depends on core, qdrant client, embedder; never on aief_pipeline
│       ├── src/aief_knowledge_mcp/
│       └── tests/
├── pipelines/                      # PipelineDefinition YAML examples (real definitions per deployment)
├── deploy/
│   ├── compose.yaml                # qdrant, docling-serve, pipeline-api, pipeline-worker, knowledge-mcp
│   └── Dockerfile.*                # one image per service; pipeline-api and pipeline-worker share one image
├── .env.example                    # variable names only, never values
├── .github/workflows/ci.yml        # uv sync --locked, ruff, pyright, import-linter, pytest (no network)
├── LICENSE                         # MIT
└── README.md                       # purpose, quick start, links to the framework pages
```

Why three packages: the Knowledge MCP is deployed and secured separately, so it must not carry the ingestion dependencies (LlamaIndex, Docling) or be able to import pipeline code.

## Layer contracts (import-linter)

| Contract | Rule |
| --- | --- |
| Core is pure | `aief_core` imports no `aief_pipeline`, `aief_knowledge_mcp`, `llama_index`, `docling`, `fastembed`, `qdrant_client`, `httpx`, `fastapi`, `mcp` |
| Use cases depend on ports | `aief_pipeline.application` imports no `aief_pipeline.adapters`, no `aief_pipeline.entrypoints`, no infrastructure library |
| Adapters do not call entry points | `aief_pipeline.adapters` imports no `aief_pipeline.entrypoints` |
| Knowledge MCP is isolated | `aief_knowledge_mcp` imports no `aief_pipeline` |

Wiring (choosing adapters for ports) happens only in `entrypoints`, the composition root.

## Tooling

| Tool | Use |
| --- | --- |
| uv | Workspace, Python version, lock file, running commands |
| ruff | Lint and format |
| pyright | Type checking; strict for `aief_core` |
| pytest | Unit, contract and opt-in end-to-end tests |
| import-linter | Layer contracts above |

## Conventions

- Configuration comes from environment variables (names in `.env.example`); `.env` is gitignored.
- Pipeline definitions are YAML, versioned in Git; they hold scope, filters, target collection, schedule and exclusions, never credentials.
- Tests never call real services in CI; end-to-end tests against real sources are opt-in and run only with the user's approval.
- Container images and Python dependencies are pinned (see [dependencies.md](dependencies.md)).
- The README links to the framework pages instead of copying them.
