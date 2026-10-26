# AI tooling: MCP servers, skills and agents

Source: AI Tooling for the Knowledge Base - MCPs, Skills and Agents (6488066, v2). Everything here is a recommendation; any tool can be replaced.

| Status | Meaning |
| --- | --- |
| Verified | Used and tested in the framework's own work |
| Official | Published by the vendor or the standard's authors; not tested here yet |
| Community | Third-party; review before adopting |
| Planned | Proposed by the framework; not built yet |

## Before installing anything

- Ask the user which sources they use and get approval before changing any configuration.
- Credentials are created and entered by the user. **Never ask for tokens or passwords in chat**; prefer OAuth or the provider's sign-in flow.
- Prefer project scope (`-s project`, stored in `.mcp.json`) for project tools and user scope for personal tools. Do not commit files that contain secrets.
- Third-party tools: read the code or skill first, pin versions, start read-only, prefer official tools.

## Configure MCP access securely (warn the user)

The framework's security principles stay in force (the Knowledge MCP authenticates and authorizes; source permissions are respected). The framework does **not** add permission mechanisms inside the projection or the pipelines: **whatever an account can read is what can enter the knowledge base.** Configuring accounts is the implementing organization's responsibility, but always **warn** the user:

> Give every MCP server an account with **only the permissions it needs**. An account with broader access (for example, an administrator account) can bring restricted content into the knowledge base.

Checklist to share with the user:
- One dedicated account per integration, never an administrator's personal account.
- Read-only by default; limited to the spaces, projects and boards that belong in the knowledge base; write access only where needed (for example, drafts).
- Prefer OAuth; otherwise narrow, expiring, rotated tokens. Avoid catch-all scopes.
- Secrets in environment variables or a secret manager, never in committed files or logs.
- Separate accounts per environment; isolate third-party local servers; keep a human in the loop for sensitive operations; review and revoke unused access.

Official references:
- MCP specification: [Security Best Practices](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices), [Authorization Security Considerations](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations)
- MCP docs: [Understanding Authorization](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/authorization), [Local Server Security](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/local-server-security)
- OWASP GenAI Security Project: [A Practical Guide for Secure MCP Server Development](https://genai.owasp.org/resource/a-practical-guide-for-secure-mcp-server-development/); OWASP MCP Top 10
- Each provider's documentation on service accounts, OAuth apps and token scopes

The same checklist applies to pipeline and adapter accounts; see also the [OWASP Top 10 for LLM Applications](https://genai.owasp.org/).

## 1. The aief plugin (Verified)

```
/plugin marketplace add devsinsight/ai-engineering-framework
/plugin install aief@devsinsight
```

The repository README is the authority for these steps. The tool is described in Framework Tooling - aief Claude Code Plugin (6160385, v1).

## 2. MCP servers for the sources (Verified)

Commands for Claude Code, run in the project folder. After adding them, restart the session and approve the servers; then sign in through `/mcp` where OAuth is required.

| Source | Command | Authentication |
| --- | --- | --- |
| Confluence, Jira (Atlassian) | `claude mcp add -s project --transport http atlassian https://mcp.atlassian.com/v1/mcp` | OAuth through `/mcp` |
| Azure DevOps | `claude mcp add -s project azure-devops -- npx -y @azure-devops/mcp <organization> -d core work work-items repositories wiki pipelines` | Microsoft Entra sign-in in the browser on first use; with Azure CLI installed, add `--authentication azcli` |
| Miro | `claude mcp add -s project --transport http miro https://mcp.miro.com/` | OAuth through `/mcp` |

Known issue: the Azure DevOps server may fail to get a token at first ("Connection closed", "Failed to obtain OAuth token"); reconnect it from `/mcp`, sometimes more than once.

## 3. Diagrams and models

| Need | Tool | Status | Where to install from |
| --- | --- | --- | --- |
| C4 (Technical) | Structurizr (reference implementation of C4, with an MCP server) | Official | https://docs.structurizr.com/ai |
| ArchiMate | mcp-archimate or archimate-mcp | Community | https://pypi.org/project/mcp-archimate/ · https://pypi.org/project/archimate-mcp/ |
| BPMN | BPMN MCP servers (several community projects) | Community | Compare projects on an MCP registry such as glama.ai before choosing |
| Simple diagrams | Mermaid | Format | No installation; rendered by Azure DevOps Wiki and GitHub |

Follow each project's own installation instructions; this guide does not repeat commands it has not verified.

## 4. Skills

| Skill | Status | Use |
| --- | --- | --- |
| aief:knowledge-base | Verified | This skill |
| PDF, DOCX, XLSX, PPTX document skills (Anthropic) | Official | Reading client documents (Evidence); see https://github.com/anthropics/skills |
| skill-creator (Anthropic) | Official | Building new framework skills |
| TOGAF / enterprise architecture skills (community) | Community | Read them for ideas; adopt useful ideas into framework skills respecting their licenses, rather than installing them as-is |

## 5. Agents (part of the aief plugin)

Source: Agent Workflow and Agent Workspace (6651906, v1). The aief plugin ships seven agents. They install with the plugin and appear as `aief:<name>`.

| Agent | Role | Sections |
| --- | --- | --- |
| `aief:orchestrator` | Talks with the user, plans with this skill, delegates, consolidates, and writes only after explicit approval | All |
| `aief:discovery` | Processes evidence into candidate items, glossary terms and gaps | 6 → 1-3 |
| `aief:business-architect` | Business context and business sections (BIZBOK, BPMN, DDD) | 1, 2 |
| `aief:requirements-analyst` | Features, stories, acceptance criteria, quality requirements (ISO 29148, INVEST, Example Mapping) | 3 |
| `aief:solution-architect` | Technical section and decisions (arc42, C4, MADR) | 4, 5 |
| `aief:knowledge-curator` | Key and source registries, glossary, duplicates, tags, gaps view (SKOS, KCS) | 0, 7 |
| `aief:auditor` | Checks the mandatory structure, common record, provenance and links; report only | All |

How they work together:
- **Run the orchestrator as the main session:** `claude --agent aief:orchestrator`. As the main session it can ask you questions and request approval. Invoked as a subagent, it cannot ask, so it returns a proposal with pending approvals instead.
- **Specialists only read and return results.** Everything goes through the orchestrator, which asks the user whether each change is adequate and requests permission before writing.
- **Agent Workspace:** drafts and reports are stored, after approval, in an area of the knowledge source outside sections 0-8 that is **not indexed**. When an item is validated, it moves to its final section.
- Claude Code can restrict which tools an agent uses, but not which space it writes to; the write boundary relies on the approval flow and on least-privilege accounts.
- The auditor runs a deterministic validation script first when one exists (planned by the framework).

## 6. Indexing (later stage)

See [projection.md](projection.md). The official Qdrant MCP server is for development and testing only; consumers use the framework's Knowledge MCP, never the vector database directly.
