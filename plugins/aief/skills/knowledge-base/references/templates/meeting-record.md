# Meeting Record: <YYYY-MM-DD> - <topic>

> Common record: see [_common-record.md](_common-record.md) (type `meeting-record`). Optional: a team may keep Meeting Records; the framework defines their shape, not when to create one. The record is the authority for **what was said and agreed, and when**. It is never the authority for product truth: once an agreement is applied, the changed item wins, and this record explains why it changed. The transcript is [evidence](evidence.md) (low authority).

## Summary

| Field | Value |
| --- | --- |
| Date and time | <YYYY-MM-DD, hh:mm-hh:mm> |
| Attendees | <name (role), ...> |
| Purpose | <one or two lines> |
| Consent to record | <yes: every attendee agreed before the recording started / not recorded> |
| Classification | public · internal · confidential · personal data |
| Related keys | `feature-…`, `rule-…` |

## Agreements

| # | Agreement | Items it changes (key or link) |
| --- | --- | --- |
| A1 | <one decision per row, stated so it can be applied without the transcript> | <keys> |

**Not agreed:** <proposals discussed and dropped, with the reason; they prevent the same discussion from reopening without new information>

## Actions

| Who | Action | By | Status |
| --- | --- | --- | --- |
| <name> | <action> | <YYYY-MM-DD> | open · done |

## Open questions

Each open question is also recorded as a [Knowledge Gap](knowledge-gap.md) in the work management system; this table only links to it.

| # | Question | Owner | Knowledge Gap |
| --- | --- | --- | --- |
| Q1 | <question> | <name> | <work item link> |

## Items updated

Filled after the agreements are applied. Agreements are applied within the period the team sets (for example, two working days).

| Item | Change | New version | Agreement |
| --- | --- | --- | --- |
| <link> | <what changed> | <version or revision> | A1 |

A significant decision also gets its own [ADR](decision.md) in section 5; link it here.

## Transcript

<Link to the original recording or transcript, stored intact as [evidence](evidence.md) with its timestamps and speakers. A cleaned-up excerpt or a summary below is a derivative: it never replaces the original.>

| Time | Speaker | Text |
| --- | --- | --- |
| 00:00 | <name> | <text> |

## Rules

- Get every attendee's consent before recording.
- Never edit an old record to hide a reversal: a later meeting that reverses an agreement links to the earlier record.
- An agreement that is not yet applied is not product truth: consumers read the changed item, not the agreement.
