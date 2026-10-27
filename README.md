# AI Engineering Framework

Provider-agnostic, knowledge-driven AI software engineering framework.

## Repository role

This repository contains version-controlled framework assets and implementation artifacts. Human-readable canonical knowledge may live in a configured knowledge provider such as Confluence, Azure DevOps Wiki, SharePoint, Git-based documentation, or another governed system.

Binary framework artifacts are stored under `/assets` according to ADR-004.

## Structure

- `.claude-plugin/` — declares this repository as a Claude Code plugin marketplace.
- `plugins/aief/` — the framework plugin: the `knowledge-base` skill and the agents.
- `assets/` — canonical binary assets and asset metadata (ADR-004).

## Claude Code plugin

This repository is a Claude Code plugin marketplace. The `aief` plugin ships the `knowledge-base` skill, which guides building a governed, multi-source project knowledge base that follows the framework: from capturing and structuring the knowledge to choosing the technologies and building the Tier 2 platform (pipelines, semantic projection, Knowledge MCP) in the project's own repository, with tested assets for its deterministic parts. It also ships seven agents that coordinate the work (`aief:orchestrator` plus six specialists).

Install it from a Claude Code session:

```
/plugin marketplace add devsinsight/ai-engineering-framework
/plugin install aief@devsinsight
```

On Claude Code 2.1.275 or later, one step is enough:

```
/plugin install aief --marketplace devsinsight/ai-engineering-framework
```

Claude uses the skill when a task matches it, or you can invoke it directly with `/aief:knowledge-base`. To coordinate the agents, start a session with the orchestrator:

```
claude --agent aief:orchestrator
```
