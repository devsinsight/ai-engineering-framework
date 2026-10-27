# Verification

Sources: Knowledge Ingestion Pipelines - Guide (6750209, v3), section 4; Semantic Search Technology Catalog (6717441, v3), sections 5-6; Semantic Knowledge Platform - Cloud + MCP (688162, v7), success criteria. This file summarizes them; if a page has a newer version, the page wins.

## Checks for every increment

| Check | How to prove it |
| --- | --- |
| Idempotency | Run twice; point IDs and counts do not change |
| Rebuildability | Delete the collection, run in full; the projection and its collection metadata are reproduced |
| Incremental runs | Edit one section of a page; the points of the old version are replaced by the new version, and only the changed chunks are embedded again (the rest come from the `content_hash` cache) |
| Deletions | Delete or archive an item at the source; its points disappear (or become `archived`) after the next run |
| Provenance | Every point has source provider, ID, canonical URL and version, and resolves back to the original |
| No fabrication | Items with missing fields have `metadata_complete: false` and the list of missing fields; no invented keys; missing state is `draft` |
| Exclusions | Agent Workspace pages are never indexed |
| No binaries | The projection holds references and text, never image or file content |
| Layer contracts | import-linter passes |
| Secrets | No credentials in code, logs, pipeline definitions or test fixtures |
| Run records | Every run has its steps, counts, durations and errors linked to the exact item and version |

## Retrieval quality: the golden set

Measure before tuning. Never change the embedding model, the chunking configuration or add a reranker without a measured improvement.

1. Write 20-50 representative questions with the keys of the items that should answer them, including questions with exact identifiers (keys, ADR numbers, API names).
2. Measure **recall@k** (is a correct item among the first k results?) and **MRR** (how high is the first correct result?).
3. Record the baseline with the models and settings used (they are in the collection metadata).
4. Change one thing at a time, rebuild, measure again, and keep the change only if it helps.
5. Keep the golden set in the repository and rerun it in later increments.

## Success criteria of the platform

- An agent retrieves relevant knowledge without reading the sources directly.
- Exact identifiers remain findable.
- Every answer can be traced to its authoritative source.
- Deleting and rebuilding the collection loses no authoritative knowledge.
- Changing the vector database does not change the Knowledge MCP contract.
