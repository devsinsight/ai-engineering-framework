# Canonical Assets

This directory contains canonical binary artifacts owned by the AI Engineering Framework repository.

## Layout

- `architecture/` — framework and solution architecture diagrams.
- `diagrams/` — process, sequence, domain, and supporting diagrams.
- `screenshots/` — governed screenshots used by framework documentation.
- `documents/` — binary documents that belong to the framework asset domain.
- `multimedia/` — audio/video artifacts.

## Rules

1. Each asset has one canonical path.
2. Prefer stable, descriptive kebab-case filenames.
3. Replace an asset only when it represents a new version of the same logical artifact; otherwise add a new file/version.
4. Knowledge pages may reference these files, but the repository revision is the authoritative binary version.
5. Semantic descriptions, OCR, captions, and embeddings are derivatives and are not authoritative replacements.
6. Ingestion should preserve repository, path, commit SHA, media type, and checksum when practical.

## Reference architecture asset

Target canonical path:

`assets/architecture/ai-engineering-framework.png`
