# AIEF principles applied to a knowledge base

This file **summarizes** rules from the AI Engineering Framework. It is a derivative: the authoritative text lives in the framework's canonical knowledge source (Confluence space `AIEF`, https://devsinsight.atlassian.net/wiki/spaces/AIEF). Each rule cites its source page and the version this summary was written against. If a page has a newer version, read the page; it wins over this summary.

| # | Rule | Source (page ID, version) |
| --- | --- | --- |
| 1 | AI is not the source of truth. AI may discover, analyze, propose and draft; approved knowledge is governed by an authoritative source. | AI Engineering Framework Home (65807, v7); 07 - Governance (753665, v2) |
| 2 | Every artifact has exactly one designated authority for its artifact class. Several systems may coexist, each owning different classes. | 03 - Knowledge Architecture (425986, v6); ADR-003 (1048580, v1) |
| 3 | The canonical knowledge source is pluggable: any governed, versioned system with stable IDs, access control and an API or export can serve. | ADR-003 (1048580, v1) |
| 4 | Binary assets may live in a separate asset store. Editable visuals are authoritative in their visual tool; exports are renditions. | ADR-004 (2162689, v1); ADR-005 (2719745, v1) |
| 5 | The semantic index is a projection, never an authority, and must be fully rebuildable from the sources. | ADR-001 (852001, v3); ADR-002 (720914, v2) |
| 6 | Summaries, OCR, captions, translations and embeddings are derivatives, never authority. | ADR-002 (720914, v2); Multimodal Knowledge & Artifact Ingestion (786465, v4) |
| 7 | Provenance is mandatory: source, provider ID, canonical URL, version. | Normalized Knowledge Artifact Contract (2686977, v2) |
| 8 | Adapters normalize each provider into a common contract; missing provider capabilities are documented as reduced fidelity, never fabricated. | Normalized Knowledge Artifact Contract (2686977, v2); ADR-003 (1048580, v1) |
| 9 | Knowledge gaps are first-class: agents report gaps instead of inventing missing truth. | 03 - Knowledge Architecture (425986, v6) |
| 10 | Work records (analysis, plans) live in the canonical source, anchored to a work item, and follow a KCS lifecycle; AI drafts, humans validate. | ADR-006 (5865473, v1) |
| 11 | Access is tiered: a deterministic index first; a semantic projection behind an MCP when complexity warrants it. | ADR-007 (5898241, v1) |
| 12 | Authority stays distributed, access is centralized; link sources with native links when they exist and tags always, under a key convention; transcripts are evidence. | Building the Knowledge Base - Capture Methods, Linking and Suggested Tools (6094849, v2) |
| 14 | Knowledge is structured by a small set of types sharing a common record; a Feature has two faces (knowledge page and delivery work item) joined by its key; gaps adapt to the work management system. | Building the Knowledge Base (6094849, v2), section "Knowledge Types" |
| 15 | One knowledge base holds business and technical knowledge in a mandatory common structure (sections 0-8, each with a minimum content); diagrams, methods and frameworks are recommendations; industry extensions specialize core types; separate bases are unified by migrating or federating, never by copying. | Knowledge Base Structure - Mature Frameworks and Reference Structure (6225921, v1) |
| 16 | Every relevant piece of information in any format produces a retrievable representation without replacing the original; each format has its own retrieval unit and provenance. | Multimodal Knowledge & Artifact Ingestion (786465, v4) |
| 13 | Use AI for reasoning; use deterministic software for enforcement. | 02 - Core Concepts (655361, v2); 06 - Engineering (229378, v2) |
