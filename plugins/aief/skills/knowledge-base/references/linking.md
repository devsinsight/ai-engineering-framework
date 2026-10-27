# Linking knowledge across sources

Sources: Building the Knowledge Base (6094849, v2); Knowledge Ingestion Pipelines - Guide (6750209, v2, section 5).

The hardest part of a dispersed knowledge base is **linking**, not indexing. A feature in the work item tool, its documentation pages and its diagram describe the same thing, but semantic search only knows they are *similar*. An explicit shared key makes the relationship certain, for AI agents and deterministic tools alike.

## Rule: native link when it exists, tag always

1. **Native link:** if the provider links work items to documentation natively (for example, a work item linked to a wiki page), use it. It is precise and maintained by the tool.
2. **Tag:** always add the shared tag as well. It is the universal fallback that works between any pair of sources, including those that do not integrate with each other (visual boards, static files).

## Tag convention

| Rule | Example |
| --- | --- |
| Lowercase, hyphen-separated, no spaces | `feature-checkout-payment` |
| Type prefix + stable key | `feature-…`, `domain-…`, `capability-…`, `rule-…` |
| Provider-independent: never a provider's numeric ID | `feature-checkout-payment`, not `ado-1234` |
| One key per artifact, reused in every source | The work item, its pages and its diagram all carry the same tag |

## Key registry

Tags are free text: a typo or a rename silently breaks the link. Keep a **key registry**, a single list of valid keys:

| Key | Type | Name | Owner | Status |
| --- | --- | --- | --- | --- |
| `feature-checkout-payment` | feature | Checkout payment | Product owner | active |

A deterministic check can then flag unknown or misspelled tags. The registry lives in the authoritative textual source.

## Provider notes

- **Wiki pages (for example, Confluence):** the page's **own key** goes in its Page Properties table (see [templates/_common-record.md](templates/_common-record.md)), not in a label. **Labels are traceability:** each label is the key of another item (for example, the feature a business page supports), and the ingestion pipeline turns it into a relationship with the work items and pages that carry the same key. Labels are lowercase and allow no spaces or colons, so the label is the key itself (`feature-checkout-payment`), and work items use exactly the same text as their tag.
- **Work items (for example, Azure DevOps):** tags are case-insensitive; multiple tags are separated by semicolons.
- **Visual boards (for example, Miro):** tags apply only to some object types (such as sticky notes and cards). For diagrams and frames, put the key in the frame title, or link the frame from the related page.
- **Static files (PDF, images, CSV):** put the key in the file name or in the asset metadata.

## Tags are not relationship types

A tag says items are related, not *how*. When the relationship type matters (implements, depends on, supersedes, documented by), add an explicit link as well.
