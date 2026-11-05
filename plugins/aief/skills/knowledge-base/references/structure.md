# The common structure of a knowledge base

Source: Knowledge Base Structure - Mature Frameworks and Reference Structure (6225921, v3). This file summarizes it; if the page has a newer version, the page wins.

| What | Status |
| --- | --- |
| The common structure (sections 0-8) and each section's minimum content | **Mandatory** |
| Diagrams, methods and frameworks per section | **Recommended**: choose what fits the business and the team |

## One knowledge base for business and technology

- A project has **one** knowledge base holding business and technical knowledge; traceability lives in the links between them.
- **Delivery stays in the work management system** (Epics, Features, User Stories, Tasks), linked with native links when available and tags always.
- One **logical** base fed by several **physical** sources (wiki, docs next to the code, work items, visual tool). Authority stays with each source.
- Separate bases are required **between projects**, not between business and technology.
- If an organization already has separate business and technical bases, unify them by **migrating** (then archive the originals and leave redirects) or **federating** (keep the sources, map them through keys and the index). **Never by copying.**

## Traceability chain

```
Goal → Capability → Process / Business Rule → Feature → User Story (acceptance criteria)
     → Component / API / Data → Decision (ADR) → Code / Test
```

## Sections

A diagram is a *view*: put the item's key in the diagram or frame title so it stays linked.

### 0. Catalog: how to find things
**Mandatory:** how the base is organized; the key registry ([template](templates/key-registry.md)); the source registry ([template](templates/source-registry.md)).
**Recommended:** SKOS for keys as controlled concepts (preferred label + synonyms); Dublin Core for descriptive metadata; data catalog practice (DAMA-DMBOK) for the source registry.

### 1. Business Context: why the product exists
**Mandatory:** vision and goals; stakeholders; glossary ([vision](templates/vision.md), [stakeholder](templates/stakeholder.md), [glossary](templates/glossary.md)).
**Recommended:** Business Model Canvas (Osterwalder) to align on the model; stakeholder map to identify owners and validators; **Impact Map** (Gojko Adzic) as traceability from goals to features; DDD ubiquitous language for the glossary.

### 2. Business: what the business does
**Mandatory:** capability map; key processes; business rules; business information (main entities and their meaning) ([domain / capability](templates/domain.md), [process](templates/process.md), [business rule](templates/business-rule.md), [business information](templates/business-information.md)).
Business rules stay here even when they are specific to the industry (a game's scoring rules, a bank's lending rules); section 8 is only for knowledge whose *structure* the core types cannot hold.
**Recommended:** capability map (BIZBOK; describe *what*, not *how*; 2-3 levels; use capabilities as the backbone for keys); value streams (BIZBOK, Lean); BPMN for critical processes only (one process per diagram); Event Storming and Domain Storytelling (DDD) for discovery; customer journey map; business rules as single testable statements with examples (ISO/IEC/IEEE 29148, BABOK).

### 3. Product: what the product offers
**Mandatory:** one knowledge page per feature (rules applied, states and flows, edge cases, dependencies, open gaps, readiness), linked to its work item; quality requirements ([feature](templates/feature.md), [quality requirement](templates/quality-requirement.md)).
**Recommended:** **User Story Map** (Jeff Patton) as traceability from the journey to the backlog; Example Mapping (BDD) per story; acceptance criteria with an ID each and exact values, written in Given/When/Then for flows, as a rule plus an examples table for data-driven cases, or as one EARS statement ("When <trigger>, the <system> shall <response>") for a single trigger and response ([user story](templates/user-story.md)); quality attribute scenarios (arc42, ISO/IEC 25010) that are measurable; UML state machines for state-driven features.

### 4. Technical: how it is built
**Mandatory:** system context; containers and components; data; APIs and integrations; technical standards ([technical standard](templates/technical-standard.md)).
**Recommended:** C4 levels 1-3; arc42 as the outline (skip what does not apply); UML sequence diagrams for non-obvious interactions; ER data model aligned with the glossary; deployment diagram; data flow diagram for security (STRIDE, trust boundaries); **capability → component map** (BIZBOK/TOGAF) and **Context Map** (DDD) as traceability; **ArchiMate layered view** when the organization already practices enterprise architecture (free tool: Archi).

### 5. Decisions: why things are the way they are
**Mandatory:** one ADR per significant decision, business or technical: context, decision, alternatives, consequences, status, date, who decided.
**Recommended:** MADR template ([template](templates/decision.md)); never delete superseded decisions; tag each ADR with the keys it affects.

### 6. Evidence: source material not yet curated
**Mandatory:** origin, date, participants (with consent for sessions), classification, related keys, and the items curated from it ([template](templates/evidence.md)).
Transcripts are stored intact, with timestamps, speakers, consent and classification. A team may also keep a **Meeting Record** (optional; [template](templates/meeting-record.md)): agreements linked to the item versions they produced, open questions linked to their Knowledge Gaps, and the transcript as evidence.
**Recommended:** SECI externalization (curate rules and decisions into sections 1-5); timestamped transcripts with speakers.

### 7. Knowledge Gaps: what we do not know yet
**Mandatory:** a view of open gaps linked to the work items that own them: question, kind, impact, owner, status.
**Recommended:** RAID-style classification (question, assumption, conflict, dependency); Example Mapping questions become gaps.
**Existing gap register.** If the project already keeps its gaps somewhere else (for example, a governed wiki page with Q-01, Q-02, ...), never copy them. Either **migrate** (create one work item per gap with its existing ID, then turn the page into a view or a redirect) or **federate** (keep the page as the source of the gaps, record it in the source registry with reduced fidelity: no owner field, no links to work items). Federating departs from the reference, so the user decides and the decision is recorded. Until then, report each gap that exists in only one place.

### 8. Industry Extensions: what is specific to this business
Use an extension only when an item needs fields or sections a core type does not have; a rule that fits the Business Rule template is a Business Rule, whatever the industry.
**Mandatory:** each extension type declares its name and purpose, the **core type it specializes**, its minimum structure, its authority class and its section ([template](templates/extension-type.md)).
**Recommended examples:** Regulation and Risk control (finance, specialize Business Rule); Clinical protocol (healthcare, specializes Process); Protected data element (healthcare, specializes Business information); Pricing policy (retail, Business Rule); Legal norm (public sector, Business Rule); Game mechanic (games, specializes Feature).

## Traceability matrix (recommended)

A requirements traceability matrix (ISO/IEC/IEEE 29148, BABOK) audits requirement → design → code → test. With consistent keys it can be generated from the index instead of maintained by hand.

## Why the structure helps the index

Section, type and key become metadata in the projection: precise filters, traceability through keys instead of similarity, and a clear separation of curated knowledge from evidence and gaps.
