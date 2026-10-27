# Ingestion rules for the adapters and the pipeline

Sources: Knowledge Ingestion Pipelines - Guide (6750209, v2), sections 4-8; Qdrant Reference Implementation (6782977, v2), section 5; Normalized Knowledge Artifact Contract (2686977, v3); Multimodal Knowledge & Artifact Ingestion (786465, v5). This file summarizes them; if a page has a newer version, the page wins.

## Pipeline rules

- Fill the contract fields (key, section, type, state, source, version) in a deterministic transformation step; never guess them with AI.
- Exclude the **Agent Workspace** (pages outside sections 0-8; configured per pipeline definition).
- Deterministic IDs and content hashes; reprocess only what changed; **propagate deletions**.
- Preserve provenance; report **reduced fidelity** instead of fabricating fields.
- Record the embedding models and the chunking configuration in the **collection metadata**; changing either requires a rebuild; never mix vectors from different models.
- Use dedicated, least-privilege, **read-only** accounts for every source.

## Metadata from wiki pages (Confluence)

| Field | Source |
| --- | --- |
| `section` | The page tree: the 0-8 section the page belongs to |
| `key` (the page's own) | Page Properties (the `details` macro), validated against the key registry |
| `artifact_type` | Page Properties |
| `lifecycle.state` | Page Properties; a page archived in the wiki becomes `archived` |
| Labels | Traceability: each label is the key of **another** item and becomes a `relationship` |

When a field is missing (default, option A): index the item with `metadata_complete: false` and the list of missing fields, and include it in the run report. No state means `draft`. No key means no key. An unregistered label is a finding for the knowledge curator.

The Page Properties table is metadata: it goes to the payload and is **not** embedded.

## Chunking

1. By structure with Docling `HybridChunker`, for pages and attachments alike.
2. Token limit = the dense embedding model's limit, measured with its tokenizer (512 for `bge-base-en-v1.5`), configured per collection.
3. Prefix each chunk with the page title and heading path (deterministic context, no AI).
4. No overlap.
5. Chunk ID derived from artifact ID, heading path and position; one `content_hash` per chunk.
6. No stored parents: consumers follow the link to the source.

| Content | Rule |
| --- | --- |
| Tables | Whole if they fit; otherwise split by rows, repeating the header |
| Code blocks | Whole if they fit; never cut inside a line |
| Work items | One chunk per item (title, description, acceptance criteria); split by field if too long |
| Miro frames | One chunk per frame; if too long, split by groups of nodes, keeping the full structure in the payload |
| Images | Their deterministic text stays in the chunk of the section where they appear; the link goes to the payload |

## Images

- Never store binaries in the projection and never copy them to another repository. Binaries are downloaded only temporarily, to parse or run OCR.
- Index a **reference** (attachment path or URL, version, page) plus **deterministic text**: alternative text, caption, surrounding text, OCR.
- The Knowledge MCP returns the link; the consumer opens it with its own read access.
- Vision descriptions (`ImageDescriber` port) are optional and **off** by default. When enabled they record model, model version and prompt version, are cached by image hash, and are never authoritative.

## Azure DevOps

Custom reader on the REST API: query with WIQL, then read in batches. One document per work item: title, description, acceptance criteria, tags, state, link. Tags with the same text as wiki labels create the cross-source links. The work item tool remains the authority for delivery data.

## Miro (REST API v2)

Ingest the boards listed in the source registry (approach B), one chunk per frame, or the whole board when it has no frames. The registry can limit a board to specific frames.

| Part | Content |
| --- | --- |
| Readable text (embedded) | Frame title, nodes with text and type, relationships written as "A → B: caption" |
| Structure (payload) | Items with ID, type, text, position, size, style, parent; connectors with start, end, caption, style |
| Provenance | Board ID, item IDs, link, modification dates |

| Need | API fact (verified October 2026) |
| --- | --- |
| One item | `GET /v2/boards/{board_id}/items/{item_id}` |
| Items in a frame | `GET /v2/boards/{board_id}/items?parent_item_id={frame_id}`, up to 50 per page, direct children only: walk nested groups |
| Connectors | `GET /v2/boards/{board_id}/connectors`: no filter by frame; list all and keep those whose ends are in the frame |
| Changes | No "modified since" filter; compare `modifiedAt` |
| Image export | Not available |

Wiki links to a board or item become `relationships`.

## Collection design (Qdrant)

| Element | Design |
| --- | --- |
| Collection | One per project; the framework uses `framework-knowledge` |
| Vectors | `text_dense`, `text_sparse` (IDF modifier); optional `image` |
| Collection metadata | Embedding models and versions; chunking configuration |
| Point ID | Deterministic UUID derived from the artifact ID and the chunk position (heading path); see "Open questions" |
| Payload | `schema_version`, `artifact_id`, `key`, `section`, `artifact_type`, `lifecycle.state`, `source` (`provider`, `provider_artifact_id`, `canonical_url`, `version`), `authority`, `content_hash`, `permissions.classification`, `provenance`, `relationships`, `metadata_complete` and missing fields, chunk text, heading path, position; image references and Miro structure where they apply |
| Payload indexes | `key`, `section`, `artifact_type`, `lifecycle.state`, `source.provider` |

| Consumer need | Query |
| --- | --- |
| Conceptual question | Hybrid (dense + sparse, fused), filtered by `lifecycle.state = validated` |
| Exact identifier | Sparse-weighted, or payload filter on `key` |
| Traceability | Filter by `key`, then follow the relationships |
| Section-scoped search | Hybrid filtered by `section` |

## Open questions (resolve with the user before implementing)

| Question | Pages | Impact |
| --- | --- | --- |
| Does the point ID include the source version? | 6782977 v2 includes it ("artifact ID, version and chunk position"); 6750209 v2, section 6, derives it from artifact, heading path and position only | With the version, every edit replaces all points of the artifact; without it, only changed chunks are rewritten (compare `content_hash`) and the version lives in the payload. Recommended: without the version, then align page 6782977 |
| Is `knowledge.propose_change` part of the read-only Knowledge MCP? | 688162 v6 lists it; 6914049 v5 says the Knowledge MCP never writes | Recommended: keep it out of the read-only service until the proposal flow (Agent Workspace, approval) is designed |
