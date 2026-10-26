# AI tooling: MCP servers, skills and agents

Source: AI Tooling for the Knowledge Base - MCPs, Skills and Agents (6488066, in review). Everything here is a recommendation; any tool can be replaced.

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

## 1. The aief plugin (Verified)

```
/plugin marketplace add devsinsight/ai-engineering-framework
/plugin install aief@devsinsight
```

The repository README is the authority for these steps.

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

## 5. Agents (Planned)

The aief plugin will provide role agents mapped to the common structure ([structure.md](structure.md)): Discovery (6 → 1-3), Business Architect (1, 2), Requirements Analyst (3), Solution Architect (4, 5), Knowledge Curator (0, 7) and Auditor (all). Until they exist, follow this skill's procedure directly.

## 6. Indexing (later stage)

See [projection.md](projection.md). The official Qdrant MCP server is for development and testing only; consumers use the framework's Knowledge MCP, never the vector database directly.
