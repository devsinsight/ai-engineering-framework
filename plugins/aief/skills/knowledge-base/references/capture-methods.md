# Knowledge capture methods

Recommendations, not mandatory steps. Choose what fits the client, the domain and the scenario. Source: Building the Knowledge Base (6094849, v3).

| Method | What it is | Use it when | Output into the knowledge base |
| --- | --- | --- | --- |
| **SECI model** (Nonaka and Takeuchi) | How tacit knowledge becomes explicit: Socialization, Externalization, Combination, Internalization | As the mental model for the whole effort | Meetings and transcripts = externalization; unifying sources = combination |
| **Knowledge audit / knowledge mapping** | Inventory of which knowledge exists, where, who owns it, how current it is | First step in scenario B; finding gaps in A and C | Source registry; gaps for missing owners or access |
| **Event Storming** (DDD) | Workshop that maps domain events, commands, actors, policies and rules on a timeline | Discovering business processes and rules, especially with no documentation | Domains, capabilities, business rules, glossary terms, open questions |
| **Domain Storytelling** (DDD) | Domain experts tell concrete stories drawn as pictographic diagrams | Understanding how people actually work; building shared language | Diagrams, glossary terms, process descriptions |
| **Example Mapping** (BDD) | Short session that organizes a story into rules, examples and questions | Refining a feature or story before implementation | Business rules with examples; acceptance criteria; questions → gaps |
| **Knowledge-Centered Service (KCS)** | Capture knowledge as a by-product of work: search first, reuse, improve, capture | Ongoing maintenance once the knowledge base exists | Updated items; work records anchored to work items (ADR-006) |
| **Data catalog principles** | Registry of sources with owners and descriptions | Recording which source owns each artifact class | Source registry; authority assignments |

## Meetings and transcripts

- A transcript is **evidence, not curated knowledge**. Index it with low authority and curate its decisions and rules into the authoritative source.
- Keep timestamps and speakers so consumers can cite the exact segment.
- Get **consent** before recording. Transcripts may contain personal or confidential data: classify them and restrict access accordingly.
- Never treat a statement in a transcript as validated product truth until its owner validates the curated item.

## Facilitation tips for an AI assistant

- Before a session, prepare the questions from the open Knowledge Gaps.
- After a session, produce: a list of candidate items (by type), a list of new gaps, and the glossary terms mentioned. All are drafts for the owners.
