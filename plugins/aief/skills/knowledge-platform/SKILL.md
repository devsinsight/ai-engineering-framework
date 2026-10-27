---
name: knowledge-platform
description: Guides building and operating the AI Engineering Framework (AIEF) knowledge platform - the Tier 2 reference implementation in devsinsight/aief-knowledge-platform, or an adopter's own version - a hexagonal Python service that ingests wiki pages, work items and visual boards through source adapters into a semantic projection (Qdrant by default) and serves it through a read-only Knowledge MCP, plus an Ops MCP to operate the pipelines. Use when scaffolding or extending that repository; writing source adapters (Confluence, Azure DevOps, Miro), parsing and chunking (Docling), embeddings (FastEmbed), the projection, the run repository or the job queue; building the CLI, webhooks, scheduler, Ops MCP or Knowledge MCP; choosing among the framework's technology options; or verifying rebuildability, provenance, deletions and retrieval quality.
---

# Build the knowledge platform with the AI Engineering Framework

This skill **guides** the construction of the knowledge platform: the software that turns a knowledge base into a searchable **semantic projection** behind a **Knowledge MCP** (Tier 2, ADR-007). The knowledge itself is built with the `aief:knowledge-base` skill; this one builds the machinery.

The reference implementation lives in the public repository **devsinsight/aief-knowledge-platform**. Adopters may build their own with other technologies, as long as they keep the same ports and contracts.

> **Core idea:** the projection is a rebuildable derivative. Sources keep the authority; the platform only reads them, preserves provenance and can rebuild everything from scratch.

## Non-negotiable rules

1. **The framework pages are the specification.** Read the pages listed in [references/architecture.md](references/architecture.md) before designing; when a page has a newer version than the one cited, the page wins. Never contradict a page silently.
2. **Deviations need a decision.** Choosing another option than a reference default, or changing the architecture, requires the user's approval and an ADR proposal for the framework's Decisions section.
3. **Read-only toward the sources.** The platform never writes to Confluence, the work item tool or the visual board; it never copies binaries between repositories.
4. **Never fabricate metadata.** Missing fields are indexed with `metadata_complete: false` and reported; a missing state is `draft`; a missing key stays missing.
5. **Rebuildable and idempotent.** Deterministic point IDs and content hashes; running twice changes nothing; deleting the collection and running again reproduces it; deletions at the source propagate.
6. **Secrets never enter chat, code or logs.** Use environment variables or a secret manager; never ask the user for tokens or passwords in chat; recommend dedicated least-privilege, read-only accounts.
7. **Never pin versions from memory.** Resolve and verify current versions when building ([references/dependencies.md](references/dependencies.md)).
8. **Ask before acting outside the working tree:** creating repositories, pushing, opening pull requests, running against real sources, or rebuilding or deleting a collection.

## Procedure

Work through the steps in order. Each step ends with a small pull request and the user's confirmation before the next one. Skip what does not apply.

### 0. Confirm the scope

- Confirm that Tier 2 is justified (several sources, multimodal content, heterogeneous permissions, or a corpus too large for direct reading). If not, stop: Tier 1 needs no platform (see `aief:knowledge-base`, step 9).
- Confirm which sources come first (default rollout: Confluence, then Azure DevOps, then Miro) and where the repository lives.

### 1. Confirm the options

Present each concern with its reference default and ask whether the project keeps it: metadata, chunking, embeddings, reranker, images, vision, visual boards, projection, pipeline service. The defaults and the pages that list the alternatives are in the `aief:knowledge-base` skill, `references/projection.md`, section "Reference defaults and options". Record any deviation as an ADR proposal (rule 2).

### 2. Prepare the toolchain and versions

Install or verify `uv` and Docker, choose the Python version, and resolve current library versions and image tags. See [references/dependencies.md](references/dependencies.md).

### 3. Scaffold the repository

Create the uv workspace with three packages (`core`, `pipeline`, `knowledge-mcp`), the tooling (ruff, pyright, pytest, import-linter), CI, the compose file and an example pipeline definition. See [references/repo-layout.md](references/repo-layout.md).

### 4. Build the walking skeleton

One thin slice from end to end: one Confluence page → contract → chunks → embeddings → Qdrant → `search` in the Knowledge MCP. It proves that the layers fit before any of them grows. See [references/walking-skeleton.md](references/walking-skeleton.md).

### 5. Grow in increments

One increment per pull request, each with acceptance criteria and tests:

1. **Confluence adapter, complete:** spaces and page trees, Page Properties, labels as relationships, attachments, images by reference, archived pages, Agent Workspace exclusion, incremental runs and deletions. See [references/ingestion.md](references/ingestion.md).
2. **Run repository and job queue:** every run, step result and error recorded; one active job per collection; retries with backoff.
3. **Inbound ports:** CLI, then REST webhooks, then the scheduler, then the **Ops MCP** with its approval levels. See [references/architecture.md](references/architecture.md).
4. **Knowledge MCP tools:** search, get context, get document, get decisions, get related, get gaps, with provenance in every result.
5. **Azure DevOps adapter**, then **Miro adapter** (one chunk per frame, structure in the payload).

### 6. Verify every increment

Run the checks in [references/verification.md](references/verification.md): idempotency, rebuild, deletions, provenance, metadata flags, exclusions, layer contracts. Before changing an embedding model, a chunking setting or adding a reranker, build a golden set and measure.

### 7. Run and operate

Run the services with docker compose; configure one least-privilege account per source; operate through the CLI or the Ops MCP. Read-only Ops MCP tools need no approval; actions need the user's confirmation; `rebuild_collection` needs explicit approval.

## How to work

- **Test first** for the domain and the use cases; adapters get **contract tests** against recorded responses, so CI never calls real services.
- Keep the **hexagonal boundaries**: the core imports no third-party infrastructure; use cases depend only on ports; wiring happens in the entry points. import-linter enforces it in CI (software enforcement before prompt enforcement).
- One branch and one pull request per step or increment; describe what was verified and how.
- Cite the framework page (ID and version) when a design choice comes from it. Separate what is **specified** (cited), what is **recommended**, and what is a **gap** to resolve with the user.
- When the code reveals that a page is wrong or incomplete, report it and propose the page change; do not let code and documentation drift apart.
