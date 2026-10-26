# Key registry

> Section 0 (Catalog). The single list of valid keys (tags). Keys follow the convention in [../linking.md](../linking.md). Treat each key as a controlled concept (SKOS): one preferred label, optional synonyms.

| Key | Type | Preferred label | Synonyms | Owner | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `capability-<key>` | capability | <name> | <alternative names> | <person or role> | active · deprecated | <replaced by…> |
| `feature-<key>` | feature | <name> | | | active | |

Rules:
- Add a key here **before** using it as a tag in any source.
- Never reuse a deprecated key for something else; point to its replacement instead.
