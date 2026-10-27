# Knowledge types

Source: Building the Knowledge Base - Capture Methods, Linking and Suggested Tools (6094849, v3), section "Knowledge Types"; 03 - Work Products (8421377, v2), the catalog of every work product with its owner role and template. This file summarizes them; if a page has a newer version, the page wins.

Items of the same type share the same structure, so consumers know where each piece of information is. Keep the set small; if a project needs another type, add it following the same pattern (common record + minimum structure + authority class).

## Common record (every item, in any source)

| Field | Meaning |
| --- | --- |
| key | Stable tag, provider-independent (see [linking.md](linking.md)) |
| type | One of the types below |
| title | Human-readable name |
| source, ID, URL, version | Where the authoritative item lives (provided by the source system) |
| owner | Who answers for the content |
| state | `draft` · `validated` · `archived` (`draft` covers the KCS states Work in Progress and Not Validated; see [contract.md](contract.md)) |

## Types

Authority classes come from the framework: textual knowledge, editable visual, binary asset, work item, source code.

| Type | What it is | Minimum structure | Authority class | Template |
| --- | --- | --- | --- | --- |
| **Vision** | Why the product exists | Problem, goals, scope, out of scope | Textual knowledge | [vision](templates/vision.md) |
| **Glossary** | Domain terms (ubiquitous language) | Term, definition, synonyms, related keys | Textual knowledge | [glossary](templates/glossary.md) |
| **Domain / Capability** | Areas of the product | Description, contained features | Textual knowledge | [domain](templates/domain.md) |
| **Feature** (anchor) | A complete piece of functionality | Summary, rules applied, states and flows, edge cases, dependencies, open gaps, readiness K0-K5 | Textual knowledge + work item, joined by the key | [feature](templates/feature.md) |
| **Business Rule** | A business rule | Statement, rationale, examples, features it applies to | Textual knowledge | [business-rule](templates/business-rule.md) |
| **Decision (ADR)** | Why something was decided | Context, decision, alternatives, consequences (MADR) | Textual knowledge | [decision](templates/decision.md) |
| **User Story** | A slice of a feature | Story, acceptance criteria (Given/When/Then), feature key | Work item | [user-story](templates/user-story.md) |
| **Diagram** | A visual view | What it shows, related keys; key in the title | Editable visual | [diagram](templates/diagram.md) |
| **Evidence** | Uncurated source material | Origin, date, participants, related keys; low authority | Binary asset | [evidence](templates/evidence.md) |
| **Knowledge Gap** | Something unknown or contradictory | Question, kind, impact, owner, status | Work item | [knowledge-gap](templates/knowledge-gap.md) |

## The two faces of a Feature

A Feature exists in two places on purpose, as in everyday practice (for example, a work item linked to its documentation page):

- the **work item** owns delivery data: state, iteration, assignee, estimate;
- the **textual page** owns knowledge: rules, flows, edge cases, decisions.

They are joined by the shared key (and a native link when available). Delivery data is never copied into the page, and knowledge is never kept only in the work item.

## Readiness K0-K5 (Feature only)

K0 Unknown · K1 Discovered · K2 Documented · K3 Business validated · K4 Implementation ready · K5 Implemented and verified. Source: Knowledge Architecture (425986, v8).
