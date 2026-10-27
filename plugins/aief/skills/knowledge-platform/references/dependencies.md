# Toolchain, dependencies and versions

Sources: Proposed Architecture - Knowledge Pipeline Service (6914049, v5), section 8; Semantic Search Technology Catalog (6717441, v3). Library names are reference defaults; **versions are never taken from this file or from memory**.

## Toolchain

| Tool | How to get it |
| --- | --- |
| uv | Official installer, user scope (no administrator): `irm https://astral.sh/uv/install.ps1 \| iex` on Windows PowerShell, `curl -LsSf https://astral.sh/uv/install.sh \| sh` elsewhere. Ask before installing |
| Python | Managed by uv (`uv python install`, `.python-version`). Choose a version that every dependency publishes wheels for; Docling and its model runtime usually lag behind the newest Python |
| Docker and Docker Compose | For Qdrant, docling-serve and the services |

## Reference libraries

| Concern | Library or image | Notes |
| --- | --- | --- |
| Ingestion engine | LlamaIndex (core, Qdrant vector store, readers as needed) | Only inside outbound adapters |
| Parsing and chunking | Docling (`HybridChunker`), through `docling-serve` or the library | See "Open questions" |
| Embeddings | FastEmbed | Dense `BAAI/bge-base-en-v1.5`, sparse `Qdrant/bm25` (IDF modifier on the collection) |
| Projection | `qdrant-client`; image `qdrant/qdrant` | Local with Docker or Qdrant Cloud |
| HTTP clients | httpx | Source adapters that call REST APIs directly |
| REST API and webhooks | FastAPI | |
| MCP servers | Official MCP Python SDK | Ops MCP and Knowledge MCP |
| CLI | A standard Python CLI library | |
| Persistence | SQLite, then PostgreSQL | |

## Resolving versions

1. Let uv resolve the newest compatible releases (`uv add <package>`), then commit `uv.lock`; CI runs `uv sync --locked`.
2. Pin container images to an exact tag, never `latest`. Get the tag from the project's GitHub releases or its registry, and confirm it exists before writing it.
3. Read the current documentation of each library before using an API; signatures change between releases (for example, `DoclingNodeParser` takes a `chunker` argument and defaults to `HierarchicalChunker`, so `HybridChunker` must be passed explicitly).
4. Record the resolved versions in the pull request description.

## Open questions (resolve when building, with the user)

| Question | Why it matters | How to resolve |
| --- | --- | --- |
| Does the current `docling-serve` release expose a chunking endpoint? | If yes, the worker stays light (no model runtime); if no, the worker image runs the Docling library and `HybridChunker` itself | Read the docling-serve API documentation for the pinned release |
| Which Qdrant release to pin? | Hybrid queries, sparse IDF and payload indexes must be supported | Qdrant GitHub releases |
| Which Python version? | Wheels for Docling and its dependencies | Check each package's supported versions |
