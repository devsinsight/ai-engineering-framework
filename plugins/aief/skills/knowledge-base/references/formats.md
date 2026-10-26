# Processing knowledge by format

Source: Multimodal Knowledge & Artifact Ingestion (786465, v4); ADR-002 (720914, v2). This file summarizes them; if a page has a newer version, the page wins.

This file says **what** each format must produce and **what provenance** to keep. It does not prescribe how to implement a parser.

**Knowledge Preservation Principle:** relevant information in pages, attachments, images, diagrams, tables or multimedia must produce a retrievable representation, without replacing or losing the original. Originals stay in their authoritative source; derivatives (text, descriptions, OCR, transcripts, embeddings) are never authority.

| Format | Retrieval unit | Preserve | Avoid |
| --- | --- | --- | --- |
| Wiki pages, DOCX | Section, by headings | Headings, paragraphs, tables, embedded media | Chunking by arbitrary character counts when structure exists |
| PDF | Page and semantic section | Page numbers, headings; tables and important images as child items | One embedding for the whole document |
| Presentations (PPTX) | Slide | Title, visible content, speaker notes, tables, slide number, visual descriptions | Merging slides into one text |
| Spreadsheets (XLSX, CSV) | Workbook → sheet → logical table or range | Headers, table names, cell ranges, sheet provenance | Flattening the workbook into prose |
| Images, diagrams | The visual object | Description of components, relationships and labels; visible text; link to the original | Relying on OCR alone (it is a fallback) |
| Editable diagrams (visual tool) | The board, frame or object | Structure read from the tool (objects, connectors, texts); key in the title; link to the editable source | Treating an exported image as the authority |
| Audio, video | Meaningful segment | Original recording; timestamped transcript; speakers | Indexing a recording without a transcript |
| Work items | The work item | ID, type, state, tags, links, acceptance criteria | Copying delivery data into knowledge pages |

## Questions to add to the knowledge audit

- Which formats exist in each source, and **how many** items of each? (3 PDFs and 4,000 recordings lead to very different decisions, including Tier 1 vs Tier 2.)
- Which items are originals and which are exports or copies?
- Are there recordings that need consent or contain personal data?

## Binary transfer

Preparing an upload is not the same as completing it. Never record that a binary was stored until the bytes were transferred and verified (provider ID, size or checksum).

## Helpful tools (evaluate, not required)

- Reading client documents: Anthropic's document skills for PDF, DOCX, XLSX and PPTX (see [tooling.md](tooling.md)).
- Editable diagrams: read them through the visual tool's MCP server instead of exporting images.
