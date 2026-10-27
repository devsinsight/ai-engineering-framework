<!-- Common record: include it at the top of every item (as page properties, front matter or work item fields). -->
<!-- In a wiki such as Confluence, put this table inside a Page Properties macro: the ingestion pipeline reads key, type and state from it (Knowledge Ingestion Pipelines - Guide, 6750209, v2, section 5). -->
| Field | Value |
| --- | --- |
| key | `<type>-<stable-key>` |
| type | `<type>` |
| title | <title> |
| source / ID / URL / version | <provided by the source system> |
| owner | <person or role> |
| state | draft |

<!--
- key: this item's own key, registered in the key registry. Never invent one; leave it empty and record a gap if it is unknown.
- state: draft, validated or archived. A missing state is treated as draft.
- section: do not add it here; it comes from the place of the page in the 0-8 structure.
- Labels or tags on the page: the keys of OTHER related items (for example, the feature this business rule applies to). They become traceability links to the work items and pages that carry the same key.
-->
