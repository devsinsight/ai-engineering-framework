---
name: knowledge-base
description: Guides building a project knowledge base that follows the AI Engineering Framework (AIEF) - authority stays distributed across the sources that own each kind of knowledge, and access is centralized through one index. Use when starting, auditing, structuring or unifying a knowledge base; inventorying knowledge sources (wikis, work items, visual boards, static files, meeting transcripts); choosing knowledge capture methods with a client; designing cross-source tags and keys; defining knowledge types and templates; or planning ingestion into a searchable index or semantic projection (for example, Qdrant behind an MCP).
---

# Build a knowledge base with the AI Engineering Framework

This skill **guides** the construction of a knowledge base. It does not enforce rules and it does not replace the people who own the knowledge.

Think of the knowledge base as a **library**: it holds the knowledge and an index to find it. It is consumer-agnostic: an AI agent, a deterministic tool or a person can query it. Enforcement belongs to those consumers, not to the library.

> **Core idea:** authority stays distributed across the sources that own each kind of knowledge; access is centralized through one index.

## Non-negotiable rules

These come from the framework's principles. See [references/principles.md](references/principles.md) for each rule and its canonical source.

1. **Never invent product truth.** If something is unknown or contradictory, record a knowledge gap instead.
2. **Every artifact has exactly one authoritative source** for its class. Copies, summaries, translations, embeddings and indexes are derivatives.
3. **Provenance is mandatory.** Every item carries its source, its ID, a URL and its version.
4. **The index is rebuildable.** Deleting the index or semantic projection must never lose knowledge.
5. **AI proposes, humans validate.** Content you draft is `draft` until an authorized person validates it.
6. **Ask before writing to any source system** (wiki, work item tool, board). Show what you intend to create or change, and wait for explicit approval.

## Procedure

Work through these steps in order, and confirm the result of each step with the user before moving on. Skip the steps that do not apply to the scenario.

### 1. Identify the starting scenario

Ask how the knowledge exists today, then choose the entry point. See [references/scenarios.md](references/scenarios.md).

| Scenario | Situation | Start with |
| --- | --- | --- |
| A. No documentation | Knowledge lives in people's heads | Capture sessions (step 5) |
| B. Documented but dispersed | Several tools hold different parts | Knowledge audit (step 2) |
| C. Centralized | One governed system holds most of it | Step 2, kept light |

### 2. Run a knowledge audit

Build a **source registry**: which sources exist, what each holds, who owns it, how current it is, and how it can be accessed (API, export, connector). Record missing access or ownership as gaps. Do not assume what a source contains: inspect it, or ask.

### 3. Assign authority by artifact class

For each class of knowledge (textual knowledge, editable visuals, binary assets, work items, source code), name the **one** source that is authoritative. Use [references/knowledge-types.md](references/knowledge-types.md) for the classes. When two sources overlap, the user decides which one owns the class; record that decision.

### 4. Define the linking keys

Agree on a **tag convention** and start a **key registry**, so that a work item, its documentation page and its diagram can be linked across tools. Prefer the provider's native link when one exists, and always add the tag. See [references/linking.md](references/linking.md).

### 5. Capture and curate knowledge

Recommend capture methods that fit the scenario: SECI, knowledge audit, Event Storming, Domain Storytelling, Example Mapping or KCS. See [references/capture-methods.md](references/capture-methods.md).

Treat transcripts and client documents as **evidence**: index them with low authority, and curate the decisions and rules they contain into the authoritative source. Recording requires consent.

### 6. Structure knowledge by type

Use the framework's knowledge types and their minimum structure: Vision, Glossary, Domain/Capability, Feature, Business Rule, Decision, User Story, Diagram, Evidence and Knowledge Gap. Each item carries the common record (key, type, title, source/ID/URL/version, owner, state). See [references/knowledge-types.md](references/knowledge-types.md) and [references/templates/](references/templates/).

### 7. Record knowledge gaps

Every unanswered question, assumption, conflict or missing dependency becomes a **Knowledge Gap** in the work management system, with an owner and an impact. Use the provider's dedicated type if it has one; otherwise use the closest type plus the tag `knowledge-gap`. See [references/templates/knowledge-gap.md](references/templates/knowledge-gap.md).

### 8. Plan the index and the projection

Decide how consumers will reach the knowledge:

- **Tier 1:** a deterministic index of items (ID, version, URL, type, key) plus direct reads from the sources.
- **Tier 2:** a semantic projection (for example, Qdrant) behind an MCP server, with both semantic search and exact lookup by key or ID.

Choose Tier 2 when there are several sources, multimodal content, heterogeneous permissions, or a corpus too large for direct reading. See [references/projection.md](references/projection.md).

## How to respond

- Keep each step small and confirm it with the user before continuing.
- Cite the framework page (ID and version) when a recommendation comes from the framework.
- Separate clearly what is **known** (cited), what is **recommended**, and what is a **gap**.
- Never present a draft as validated knowledge.
