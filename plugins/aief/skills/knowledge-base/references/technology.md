# Technology options and reference defaults (Tier 2)

Sources: Semantic Search Technology Catalog (6717441, v3); Knowledge Ingestion Pipelines - Guide (6750209, v3), sections 4-8; Qdrant Reference Implementation (6782977, v2). This file summarizes them; if a page has a newer version, the page wins.

Every technology is an **option**. The framework names a **reference default** for each concern. Recommend it unless the user has a reason to choose otherwise; a deviation is the user's decision, recorded as an ADR. Claims come from documentation reviewed in October 2026: verify current versions, licenses and prices before adopting.

## Summary of defaults

| Concern | Reference default |
| --- | --- |
| Projection | **Qdrant** (local with Docker; Qdrant Cloud later) |
| Dense embeddings | **`BAAI/bge-base-en-v1.5`** (768 dimensions, MIT) through FastEmbed |
| Sparse embeddings | **`Qdrant/bm25`** through FastEmbed (IDF modifier on the collection) |
| Chunking | **By structure**: Docling `HybridChunker`, token limit of the dense model, heading path as context, no overlap |
| Reranker | **None** until a golden set shows the need |
| Images | **Reference plus deterministic text** (alternative text, caption, surrounding text, OCR) |
| Vision model | **Off** |
| Image repository | **None**: reference images where they already are |
| Visual boards (Miro) | **Read by API, one chunk per frame**; board structure in the payload |
| Metadata from wiki pages | **Section from the page tree; key, type and state from Page Properties; labels as traceability**; missing fields indexed and flagged |
| Pipeline service | **Hexagonal Python service** with LlamaIndex in the outbound adapters (see [platform.md](platform.md)) |

## Projection

Must have: hybrid search (dense + sparse), payload filtering, rebuildable deterministic loading.

| Situation | Option |
| --- | --- |
| Starting a project, small team, local first | **Qdrant** (Docker), later Qdrant Cloud |
| Most mature built-in hybrid search and vectorization | Weaviate |
| Very large corpus (hundreds of millions of items) | Milvus / Zilliz |
| Organization standardized on PostgreSQL | pgvector |
| Organization already runs Elasticsearch / OpenSearch | Elasticsearch / OpenSearch |
| No operations capacity | Pinecone, or a cloud service (Azure AI Search, Vertex AI Vector Search, Amazon OpenSearch Service, MongoDB Atlas Vector Search) |
| Quick local experiment | Chroma |

Switching cost: low for consumers (the Knowledge MCP contract does not change); rebuild the projection from the sources.

## Embeddings

Rules: the model is configuration per collection; record it in the collection metadata; changing it requires a rebuild; never mix vectors from different models; measure before switching. The knowledge base is in English; use a multilingual model only when it is not.

| Situation | Dense | Sparse |
| --- | --- | --- |
| Starting a project | **`bge-base-en-v1.5`** | **`bm25`** |
| Modest hardware or very large corpus | `bge-small-en-v1.5` (384) | `bm25` |
| Golden set shows missed relevant chunks | `mxbai-embed-large-v1` or `bge-large-en-v1.5` (1024) | then try SPLADE++ (`prithivida/Splade_PP_en_v1`) |
| Same size class as the default, to compare | `snowflake-arctic-embed-m`, `nomic-embed-text-v1.5` (needs task prefixes) | `bm25` |
| No capacity to run models | Hosted API (OpenAI, Azure OpenAI, Voyage AI, Cohere) only if the content classification allows content to leave the organization | `bm25` |
| Knowledge base not in English | Multilingual model (for example `intfloat/multilingual-e5-large`) | `bm25` configured for the language |

`Qdrant/bm42` is for experiments only.

## Chunking

| Strategy | When to use |
| --- | --- |
| **By structure (default)** | Wiki pages, PDF and Office documents |
| Sentence or recursive | Text without headings |
| Fixed size with overlap | Unstructured plain text such as transcripts |
| Semantic | Long unstructured documents, after measuring |
| LLM-generated context | Only if the golden set justifies the cost |

## Reranker

Default: none. Add one when the right chunk usually appears in the top 20 but not in the top 5.

| Option | When to use |
| --- | --- |
| `Xenova/ms-marco-MiniLM-L-6-v2` | Fastest first reranker on CPU |
| `Xenova/ms-marco-MiniLM-L-12-v2` | Somewhat more precise |
| `BAAI/bge-reranker-base` | First choice when quality matters |
| Jina rerankers | Small and fast; check the license (some are non-commercial) |
| ColBERT late interaction | Near cross-encoder precision; much more storage |
| Hosted rerank APIs | No local capacity; content leaves the organization |

## Vision model (optional, off)

Enable only when images must be findable by their **visual** content (for example, diagrams with no text and no structured source). Descriptions are derivatives: record model, version and prompt version; mark them `derived`; cache them by image hash; skip decorative images and images with a structured source.

| Option | When to use |
| --- | --- |
| **No vision model (default)** | Images with text; consumers describe images on demand through the link |
| Docling presets (`granite_picture_description`, `smolvlm_picture_description`) | Content cannot leave the organization and there is no GPU |
| Local model through an OpenAI-compatible server (Ollama, vLLM) | GPU available and sensitive content |
| Hosted API | Complex diagrams, when the content classification allows it |

It plugs in behind the `ImageDescriber` port (Docling `do_picture_description`, `PictureDescriptionVlmOptions` or `PictureDescriptionApiOptions`).

## Image repository (optional, none)

| Option | When to use |
| --- | --- |
| **Source in place (default)** | Most projects |
| Object storage (Azure Blob, S3, Google Cloud Storage, MinIO) | Many binaries; organizations already on a cloud provider |
| Git with LFS | Small teams that manage everything in Git |
| Digital asset management (Cloudinary, Bynder, AEM Assets) | Many design or marketing assets |

The pipeline references, never copies; the Knowledge MCP returns a link (signed when supported), never the binary; repositories with client material are private and project-specific.

## Visual boards

| Approach | When to use |
| --- | --- |
| **Driven by the board (default)** | Ingest the boards in the source registry, one chunk per frame; wiki links become relationships |
| Driven by the wiki | Only what wiki pages link to; less data, but unlinked content stays invisible |

## Metadata when a field is missing

| Option | When to use |
| --- | --- |
| **Index and flag (default)** | `metadata_complete: false` plus the missing fields, in the run report |
| Skip and report | The item must not be searchable until fixed |
| Fail the run | Strict environments where incomplete metadata must block publication |
