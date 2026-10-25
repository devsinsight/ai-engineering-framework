# AI Engineering Framework

Provider-agnostic, knowledge-driven AI software engineering framework.

## Repository role

This repository contains version-controlled framework assets and implementation artifacts. Human-readable canonical knowledge may live in a configured knowledge provider such as Confluence, Azure DevOps Wiki, SharePoint, Git-based documentation, or another governed system.

Binary framework artifacts are stored under `/assets` according to ADR-004.

## Structure

- `docs/` — version-controlled documentation supplements.
- `agents/` — agent definitions and prompts.
- `schemas/` — normalized knowledge and integration schemas.
- `generators/` — deterministic generators/templates.
- `assets/` — canonical binary assets.
- `plugins/aief/` — Claude Code plugin with the framework's skills.

## Claude Code plugin

This repository is a Claude Code plugin marketplace. The `aief` plugin currently ships one skill, `knowledge-base`, which guides building a governed, multi-source project knowledge base that follows the framework.

Install it from a Claude Code session:

```
/plugin marketplace add devsinsight/ai-engineering-framework
/plugin install aief@devsinsight
```

On Claude Code 2.1.275 or later, one step is enough:

```
/plugin install aief --marketplace devsinsight/ai-engineering-framework
```

Claude uses the skill when a task matches it, or you can invoke it directly with `/aief:knowledge-base`.
