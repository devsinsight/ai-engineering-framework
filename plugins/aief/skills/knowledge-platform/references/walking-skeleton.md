# Walking skeleton

A **walking skeleton** (Alistair Cockburn) is the thinnest implementation that runs from end to end through every layer. It proves that the architecture fits before any part grows. Decided with the framework owner (2026-10-27) as the first increment after the scaffold.

## The slice

```
CLI: run <pipeline> --item <confluence-page-id>
  → RunPipeline (use case; records a PipelineRun)
  → ConfluenceReader (one page, read-only account from the environment)
  → normalize to the contract (key, type, state from Page Properties; section from the page tree)
  → Docling: parse and chunk by structure (HybridChunker, 512 tokens)
  → FastEmbed: dense + sparse vectors
  → Qdrant: upsert with deterministic IDs; collection metadata recorded
Knowledge MCP: knowledge.search(query) → chunks with provenance
```

## In scope

- `aief_core`: the contract (artifact, chunk), `PipelineDefinition`, `PipelineRun`, `StepResult`, `RunError`, ID derivation and the policies the slice needs; ports for reader, chunker, embedder, vector store, run repository.
- `aief_pipeline`: `RunPipeline` for a single item; the four adapters above; a SQLite run repository; the CLI as entry point.
- `aief_knowledge_mcp`: one tool, `knowledge.search`, hybrid query, filtered by `lifecycle.state` (configurable for the skeleton so `draft` pages can be found).
- `deploy/compose.yaml` with Qdrant (and docling-serve if that is the chosen parsing path).
- One example pipeline definition in `pipelines/`.

## Out of scope (later increments)

Attachments, images, labels as relationships, incremental runs and deletions, job queue and worker, REST webhooks, scheduler, Ops MCP, the other Knowledge MCP tools, Azure DevOps and Miro.

## Acceptance criteria

| # | Given | When | Then |
| --- | --- | --- | --- |
| 1 | A Confluence page with Page Properties (key, type, state) | The pipeline runs for that page | Its chunks are in Qdrant with key, section, type, state and source (provider, ID, URL, version) in the payload |
| 2 | The same page, unchanged | The pipeline runs again | The point IDs and the number of points are the same (idempotent) |
| 3 | The collection is deleted | The pipeline runs again | The collection is reproduced with the same IDs and the collection metadata (rebuildable) |
| 4 | A page without Page Properties | The pipeline runs | The chunks have `metadata_complete: false`, the missing fields, state `draft` and no key |
| 5 | The page is indexed | `knowledge.search` is called with a phrase from the page | The chunk is returned with its provenance |
| 6 | The repository | CI runs | ruff, pyright, import-linter and the tests pass without network access |

Criteria 1-5 run against a real page only with the user's approval and a read-only account; CI covers them with recorded responses.
