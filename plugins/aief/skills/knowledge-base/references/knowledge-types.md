# Knowledge types

Source: Building the Knowledge Base - Capture Methods, Linking and Suggested Tools (6094849, v6), section "Knowledge Types"; 03 - Work Products (8421377, v4), the catalog of every work product with its owner role and template. This file summarizes them; if a page has a newer version, the page wins.

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
| **Stakeholder** | A person, role or group with an interest in the product | Role, interest, what they decide or validate, how to reach them | Textual knowledge | [stakeholder](templates/stakeholder.md) |
| **Process** | A key business process | Trigger, actors, steps, rules applied, outcome, owner | Textual knowledge (a BPMN diagram is a view of it) | [process](templates/process.md) |
| **Business information** | A main business entity and its meaning | Definition, key attributes, states, rules, glossary term | Textual knowledge | [business-information](templates/business-information.md) |
| **Quality requirement** | A measurable quality attribute | Quality characteristic, scenario (source, stimulus, environment, response), measure | Textual knowledge | [quality-requirement](templates/quality-requirement.md) |
| **Technical standard** | A rule for how the product is built | Rule, scope, rationale, enforcement, exceptions | Textual knowledge | [technical-standard](templates/technical-standard.md) |
| **Evidence** | Uncurated source material | Origin, date, participants, related keys; low authority | The class of the file it is (a transcript page is textual knowledge; a recording or PDF is a binary asset); its authority is always low | [evidence](templates/evidence.md) |
| **Meeting Record** (optional) | What a meeting said and agreed, and what changed because of it | Summary with consent, agreements (each linked to the items it changes), not agreed, actions, open questions (linked to their Knowledge Gaps), items updated with their new versions, transcript | Textual knowledge (the record); the transcript is Evidence | [meeting-record](templates/meeting-record.md) |
| **Knowledge Gap** | Something unknown or contradictory | Question, kind, impact, owner, status | Work item | [knowledge-gap](templates/knowledge-gap.md) |

## The two faces of a Feature

A Feature exists in two places on purpose, as in everyday practice (for example, a work item linked to its documentation page):

- the **work item** owns delivery data: state, iteration, assignee, estimate;
- the **textual page** owns knowledge: rules, flows, edge cases, decisions.

They are joined by the shared key (and a native link when available). Delivery data is never copied into the page, and knowledge is never kept only in the work item.

## Cases the classes do not answer at first sight

- **Data files next to the code** (balance tables, configuration, seed data) belong to the source-code class. When a data file and a textual page hold the same values, name one of them the authority in the source registry; the other is a derivative, ideally checked by a test.
- **Approval of a binary asset.** The image, model or recording lives in its asset store; *which* asset is approved, for what, and by whom is textual knowledge, recorded in the item that uses it (for example, a table with the asset ID and its status). A copy shown in a visual tool is a rendition and carries the same status.
- **Evidence in a textual source.** A transcript stored as a wiki page is still Evidence: the page is textual, its authority is low.

## State of existing content in a mature space

A knowledge base built over content the organization already governs (pages with owners and versions, used as reference) should not mark everything `draft` forever, nor promote it silently:

1. Items you create or draft stay `draft` until an owner validates them.
2. For existing items, a missing state is treated as `draft`. Propose to each owner a **bulk confirmation per section** (the list of their items, with any gaps found in them); items the owner confirms become `validated`.
3. Record the confirmation (who, when, which items) in the Agent Workspace, and keep open gaps open: validating an item does not resolve its gaps.

## Readiness K0-K5 (Feature only)

K0 Unknown · K1 Discovered · K2 Documented · K3 Business validated · K4 Implementation ready · K5 Implemented and verified. Source: Knowledge Architecture (425986, v8).
