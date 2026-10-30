# Knowledge capture methods

Recommendations, not mandatory steps. Choose what fits the client, the domain and the scenario. Source: Building the Knowledge Base (6094849, v5).

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

- A transcript is **evidence, not curated knowledge**. Index it with low authority and curate its decisions and rules into the authoritative source. Low authority does not judge the content: it tells consumers which source wins when the transcript and a validated item disagree.
- **Store the transcript intact**, whatever the meeting. The framework does not decide which meetings are worth keeping or what to do with them later; that is the consumer's decision. Retention or deletion follows the organization's policy. A cleaned-up version or a summary is a derivative and never replaces the original.
- Keep timestamps and speakers so consumers can cite the exact segment.
- Get **consent** before recording. Transcripts may contain personal or confidential data: classify them and restrict access accordingly.
- Never treat a statement in a transcript as validated product truth until its owner validates the curated item.

### Meeting Record

A **Meeting Record** ([template](templates/meeting-record.md)) is optional: a team may keep one, typically when a meeting changes the design, the rules, the architecture or the backlog. If it does, the record closes the loop between what was said and what changed:

1. **Agreements** are numbered (A1, A2, ...) and each names the items it changes. Proposals that were dropped are recorded as *not agreed*, with the reason.
2. The owners **apply** the agreements to the authoritative items within an agreed period, as new versions. A significant decision also gets an ADR.
3. The record lists the **items updated** with their new versions, so a consumer can trace any change back to the meeting and the transcript segment.
4. Every **open question** becomes a Knowledge Gap in the work management system; the record links to it. A question that exists only in the record is invisible to the gaps view.
5. A later meeting that reverses an agreement links to the earlier record; old records are never edited to hide it.

Until an agreement is applied, it is not product truth: consumers read the changed item, never the agreement. When an agreement and its target item disagree (for example, an action still open), report it as a conflict gap.

## Facilitation tips for an AI assistant

- Before a session, prepare the questions from the open Knowledge Gaps.
- After a session, produce: a list of candidate items (by type), a list of new gaps, and the glossary terms mentioned. All are drafts for the owners.
