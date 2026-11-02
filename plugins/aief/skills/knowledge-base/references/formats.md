# Processing knowledge by format

Source: Multimodal Knowledge & Artifact Ingestion (786465, v5); ADR-002 (720914, v3); Knowledge Ingestion Pipelines - Guide (6750209, v3, sections 6-8). This file summarizes them; if a page has a newer version, the page wins.

This file says **what** each format must produce and **what provenance** to keep. It does not prescribe how to implement a parser.

**Knowledge Preservation Principle:** relevant information in pages, attachments, images, diagrams, tables or multimedia must produce a retrievable representation, without replacing or losing the original. Originals stay in their authoritative source; derivatives (text, descriptions, OCR, transcripts, embeddings) are never authority.

| Format | Retrieval unit | Preserve | Avoid |
| --- | --- | --- | --- |
| Wiki pages, DOCX | Section, by headings | Headings, paragraphs, tables, embedded media | Chunking by arbitrary character counts when structure exists |
| PDF | Page and semantic section | Page numbers, headings; tables and important images as child items | One embedding for the whole document |
| Presentations (PPTX) | Slide | Title, visible content, speaker notes, tables, slide number, visual descriptions | Merging slides into one text |
| Spreadsheets (XLSX, CSV) | Workbook → sheet → logical table or range | Headers, table names, cell ranges, sheet provenance | Flattening the workbook into prose |
| Images, diagrams | The visual object, inside the section where it appears | A reference to the original (path or URL, version); deterministic text: alternative text, caption, surrounding text, OCR. Consumers open the link to see the image. A vision description is optional and off by default | Storing binaries in the index; copying images to another repository; treating an AI description as authority |
| Editable diagrams (visual tool) | The frame (or the board when it has no frames) | Structure read from the tool's API (items, connectors, texts, positions, styles) plus readable text, so the diagram can be understood or recreated; key in the title; link to the editable source | Treating an exported image as the authority |
| Audio, video | Meaningful segment | Original recording; timestamped transcript; speakers | Indexing a recording without a transcript |
| Work items | The work item | ID, type, state, tags, links, acceptance criteria | Copying delivery data into knowledge pages |

## Questions to add to the knowledge audit

- Which formats exist in each source, and **how many** items of each? (3 PDFs and 4,000 recordings lead to very different decisions, including Tier 1 vs Tier 2.) Count in retrieval units: pages, work items, files, and for visual boards the boards and their frames, not individual shapes or stickies.
- Which items are originals and which are exports or copies?
- Are there recordings that need consent or contain personal data?

## Reading through MCP servers: check fidelity

An MCP server is an adapter, and adapters lose things. Before concluding that content is missing or contradictory, check that the reader did not drop it:

- Simplified formats (for example, Markdown from a wiki) may render macros empty or drop them: dates, status lozenges, page-properties tables, child-page lists, embedded boards.
- Bulk listings and searches may return titles or excerpts without bodies, or cut long bodies.
- When an item matters, read it individually in the richest format the server offers (for example, HTML or the native document format), and record what could not be read as reduced fidelity in the source registry. Never report a gap that comes only from the reader.

## Binary transfer

Preparing an upload is not the same as completing it. Never record that a binary was stored until the bytes were transferred and verified (provider ID, size or checksum).

## Helpful tools (evaluate, not required)

- Reading client documents: Anthropic's document skills for PDF, DOCX, XLSX and PPTX (see [tooling.md](tooling.md)).
- Editable diagrams: read them through the visual tool's MCP server instead of exporting images.
