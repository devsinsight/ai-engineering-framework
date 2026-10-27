# Normalized Knowledge Artifact (summary for adapter builders)

Source: Normalized Knowledge Artifact Contract (2686977, v3). This file summarizes it; if the page has a newer version, the page wins.

Every source adapter translates provider-specific content into this provider-neutral model before indexing. **Normalization never changes authority**, and a missing provider capability is reported as reduced fidelity, never fabricated.

## Fields

| Field | Required | Purpose |
| --- | --- | --- |
| `schema_version` | Yes | Contract version the artifact follows |
| `artifact_id` | Yes | Stable framework identifier, independent of the provider |
| `artifact_type` | Yes | Normalized type (below) |
| `key` | Yes for knowledge base items | Linking key (tag) from the key registry |
| `section` | Yes for knowledge base items | `catalog` · `business-context` · `business` · `product` · `technical` · `decisions` · `evidence` · `knowledge-gaps` · `industry-extensions` |
| `title` | Yes | Human-readable name |
| `content` | Yes | Text, structured content and/or semantic description |
| `content_hash` | Yes | Hash of the normalized content; skip unchanged items when reindexing |
| `source` | Yes | Provider, provider artifact ID, canonical URL, version |
| `authority` | Yes | Artifact class and whether this item is the authority |
| `lifecycle` | Yes | `state` and optional `valid_from` / `valid_to` |
| `readiness` | Features only | K0-K5 |
| `relationships` | No | Typed links: `contains`, `belongs_to`, `implements`, `depends_on`, `supersedes`, `documents`, `documented_by`, `visualizes`, `derived_from`, `export_of`, `anchored_to`, `resolves` |
| `assets` | No | Referenced binaries and renditions |
| `permissions` | Yes | Provider-derived access and classification context |
| `provenance` | Yes | Discovered, modified and ingested timestamps; adapter |

## State model

| State | Meaning | KCS lifecycle |
| --- | --- | --- |
| `draft` | Proposed, not validated | Work in Progress, Not Validated |
| `validated` | Validated by an authorized person | Validated |
| `archived` | No longer current; kept for history | Archived |

- AI creates `draft`; only authorized people set `validated` or `archived`.
- "Historical" is derived: `valid_to` in the past.
- Readiness K0-K5 applies only to Features.

## Artifact types

Vision · Glossary · Domain · Capability · Feature · Rule (Business Rule) · ADR (Decision) · UserStory · KnowledgeGap · WorkRecord · Evidence · Page · Diagram · Image · Document · PDF · Spreadsheet · Presentation · AudioVideo · SourceCode · ExternalReference. Industry extension types specialize one of them.

## What the projection must keep

Chunks, embeddings, OCR, transcripts and descriptions are derivatives. Each must keep `artifact_id`, `key`, `section`, `artifact_type`, state, source identity, version, permissions and provenance, so consumers can filter precisely and trace results back to the authority.
