# Canonical Assets

This directory is the framework's **Canonical Asset Store** for the reference implementation (ADR-004). It holds binary artifacts owned by the framework repository, and the metadata of assets whose authority lives elsewhere.

## Layout

Create subfolders by kind only when an asset of that kind is added, for example:

- `architecture/` — framework and solution architecture diagrams.
- `diagrams/` — process, sequence, domain and supporting diagrams.
- `screenshots/` — governed screenshots used by framework documentation.
- `documents/` — binary documents that belong to the framework asset domain.
- `multimedia/` — audio and video artifacts.

## Rules

1. Each asset has one canonical path.
2. Prefer stable, descriptive kebab-case filenames.
3. Replace an asset only when it represents a new version of the same logical artifact; otherwise add a new file or version.
4. Knowledge pages may reference these files; the repository revision is the authoritative binary version.
5. Semantic descriptions, OCR, captions and embeddings are derivatives and are not authoritative replacements.
6. Ingestion preserves repository, path, commit SHA, media type and checksum when practical.
7. Never record that a binary is stored until the file exists and its size or checksum is verified.

## Reference architecture asset

The architecture diagram is an **editable visual**: its authority is the Miro board (ADR-005), recorded in `architecture/ai-engineering-framework.asset.json`. An exported PNG is optional and, if added, is only a snapshot.
