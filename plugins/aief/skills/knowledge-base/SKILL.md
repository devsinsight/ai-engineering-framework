---
name: knowledge-base
description: Guides building a project knowledge base that follows the AI Engineering Framework (AIEF) - one knowledge base for business and technology, organized in a mandatory common structure (catalog, business context, business, product, technical, decisions, evidence, gaps, industry extensions), with authority distributed across the sources and access centralized through one index. Use when starting, auditing, structuring or unifying a knowledge base; inventorying sources (wikis, work items, visual boards, static files, meeting transcripts); choosing capture methods, diagrams or frameworks (BIZBOK, ISO 29148, arc42, C4, DDD, BPMN); designing cross-source tags and keys; processing documents by format; setting up the MCP servers, skills and agents that support the work; choosing the access tier and the technologies (projection, embeddings, chunking, reranker, vision) from the framework's options and reference defaults; or building and operating the Tier 2 platform - a hexagonal Python service that ingests the sources into a semantic projection (Qdrant by default) behind a read-only Knowledge MCP and an Ops MCP.
---

# Build a knowledge base with the AI Engineering Framework

This skill **guides** the construction of a knowledge base. It does not enforce rules and it does not replace the people who own the knowledge.

Think of the knowledge base as a **library**: it holds the knowledge and an index to find it. It is consumer-agnostic: an AI agent, a deterministic tool or a person can query it. Enforcement belongs to those consumers, not to the library.

> **Core idea:** one knowledge base for business and technology; authority stays distributed across the sources that own each kind of knowledge; access is centralized through one index.

## Non-negotiable rules

These come from the framework's principles. See [references/principles.md](references/principles.md) for each rule and its canonical source.

1. **Never invent product truth.** If something is unknown or contradictory, record a knowledge gap instead.
2. **Every artifact has exactly one authoritative source** for its class. Copies, summaries, translations, embeddings and indexes are derivatives.
3. **Provenance is mandatory.** Every item carries its source, its ID, a URL and its version.
4. **The index is rebuildable.** Deleting the index or semantic projection must never lose knowledge.
5. **AI proposes, humans validate.** Content you draft is `draft` until an authorized person validates it.
6. **Ask before writing to any source system or changing any configuration** (wiki, work item tool, board, MCP setup). Show what you intend to do and wait for explicit approval. Never ask for tokens or passwords in chat.
7. **Technologies are options with a reference default.** Recommend the default unless the user has a reason to choose otherwise; a deviation is the user's decision and is recorded as an ADR.

## What is mandatory and what is recommended

| Mandatory | Recommended |
| --- | --- |
| The common structure (sections 0-8) and each section's minimum content | Diagrams, methods, frameworks and tools: choose what fits the business and the team |

## Procedure

Work through these steps in order, and confirm the result of each step with the user before moving on. Skip the steps that do not apply.

### 0. Prepare the tooling

Ask which systems hold the knowledge, then propose the MCP servers and skills that connect to them. Install only with approval. For larger efforts, recommend running the aief agents with the orchestrator as the main session (`claude --agent aief:orchestrator`). See [references/tooling.md](references/tooling.md) for verified commands and recommended tools.

### 1. Identify the starting scenario

Ask how the knowledge exists today. See [references/scenarios.md](references/scenarios.md).

| Scenario | Situation | Start with |
| --- | --- | --- |
| A. No documentation | Knowledge lives in people's heads | Capture sessions (step 5) |
| B. Documented but dispersed | Several tools hold different parts | Knowledge audit (step 2) |
| C. Centralized | One governed system holds most of it | Step 2, kept light |

If the organization has separate business and technical bases, plan to unify them by migrating or federating, never by copying ([references/structure.md](references/structure.md)).

### 2. Run a knowledge audit

Fill the **source registry** ([template](references/templates/source-registry.md)): which sources exist, what each holds, which **formats and how many** items, who owns it, how current it is, and how to access it. Record missing access or ownership as gaps. Do not assume what a source contains: inspect it, or ask.

### 3. Assign authority by artifact class

For each class (textual knowledge, editable visuals, binary assets, work items, source code), name the **one** authoritative source. When sources overlap, the user decides; record the decision. See [references/knowledge-types.md](references/knowledge-types.md).

### 4. Define the linking keys

Agree on the tag convention and start the **key registry** ([template](references/templates/key-registry.md)). Prefer the provider's native link when it exists, and always add the tag. See [references/linking.md](references/linking.md).

### 5. Capture and curate knowledge

Recommend capture methods that fit the scenario: SECI, knowledge audit, Event Storming, Domain Storytelling, Example Mapping or KCS. See [references/capture-methods.md](references/capture-methods.md).

Treat transcripts and client documents as **evidence**: keep them with low authority and curate their rules and decisions into the structure. Recording requires consent. Store transcripts intact; what to do with them later is the consumer's decision. If the team keeps a **Meeting Record** (optional; [template](references/templates/meeting-record.md)), it links agreements to the item versions they produced and records open questions as Knowledge Gaps. Process each format as described in [references/formats.md](references/formats.md).

### 6. Organize the knowledge in the common structure

Create the sections and fill each section's mandatory minimum, using the knowledge types and templates. Offer the recommended diagrams and methods of each section. See [references/structure.md](references/structure.md), [references/knowledge-types.md](references/knowledge-types.md) and [references/templates/](references/templates/).

| # | Section | In plain words |
| --- | --- | --- |
| 0 | Catalog | How to find things (key registry, source registry) |
| 1 | Business Context | Why the product exists |
| 2 | Business | What the business does |
| 3 | Product | What the product offers |
| 4 | Technical | How it is built |
| 5 | Decisions | Why things are the way they are |
| 6 | Evidence | Source material not yet curated |
| 7 | Knowledge Gaps | What we do not know yet |
| 8 | Industry Extensions | What is specific to this business |

Delivery (Epics, Features, User Stories, Tasks) stays in the work management system, linked by keys.

### 7. Add industry extensions when needed

When the business has knowledge the core types do not cover, declare an extension type that specializes a core type ([template](references/templates/extension-type.md)).

### 8. Record knowledge gaps

Every unanswered question, assumption, conflict or missing dependency becomes a **Knowledge Gap** in the work management system, with an owner and an impact. Use the provider's dedicated type if it has one; otherwise the closest type plus the tag `knowledge-gap`. See [references/templates/knowledge-gap.md](references/templates/knowledge-gap.md).

### 9. Choose the access tier

- **Tier 1:** a deterministic index of items (key, type, section, source/ID/URL/version, state) plus direct reads from the sources.
- **Tier 2:** a semantic projection (for example, Qdrant) behind an MCP server, with semantic search and exact lookup by key or ID.

Choose Tier 2 when there are several sources, multimodal content, heterogeneous permissions, or a corpus too large for direct reading. See [references/projection.md](references/projection.md). Adapters map every source into the common contract: [references/contract.md](references/contract.md). With Tier 1, the procedure ends here.

### 10. Choose the technologies (Tier 2)

For each concern (projection, embeddings, sparse model, chunking, reranker, images, vision, image repository, visual boards), present the reference default, when another option fits better, and the cost of switching. Ask the user to confirm or choose. See [references/technology.md](references/technology.md).

### 11. Build and operate the platform (Tier 2)

Generate the platform in the project's own repository (ask before creating it), following the framework's hexagonal architecture:

1. **Scaffold:** uv workspace with three packages (`core`, `pipeline`, `knowledge-mcp`), layer contracts enforced by import-linter, CI. Copy the tested pieces in [assets/platform/](assets/platform/) as they are; generate the rest following [references/platform.md](references/platform.md).
2. **Walking skeleton:** one wiki page → contract → chunks → embeddings → projection → `knowledge.search`, with its acceptance criteria.
3. **Grow in increments**, one pull request each: complete source adapters (wiki first, then work items, then visual boards), run repository and job queue, CLI, webhooks, scheduler, Ops MCP, the remaining Knowledge MCP tools. Apply [references/ingestion.md](references/ingestion.md).
4. **Verify every increment** and measure retrieval with a golden set before tuning: [references/verification.md](references/verification.md).
5. **Operate** with least-privilege, read-only source accounts; destructive operations (rebuilding a collection) need explicit approval.

Never pin versions from memory: resolve and verify them when building. Ask before creating repositories, pushing, opening pull requests, running against real sources, or deleting a collection. When a reusable piece has proven itself in a real project, propose adding it to the assets.

## How to respond

- Keep each step small and confirm it with the user before continuing.
- Cite the framework page (ID and version) when a recommendation comes from the framework.
- Separate clearly what is **known** (cited), what is **recommended**, and what is a **gap**.
- Never present a draft as validated knowledge.
