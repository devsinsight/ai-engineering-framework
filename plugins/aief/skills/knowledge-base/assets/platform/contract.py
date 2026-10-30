"""Normalized Knowledge Artifact contract (schema version 2) and deterministic identities.

Copy this module as-is into the platform's core package (for example
``packages/core/src/aief_core/domain/contract.py``). It uses only the standard
library, so the domain layer stays free of infrastructure.

Sources: Normalized Knowledge Artifact Contract (Confluence 2686977, v4);
Knowledge Ingestion Pipelines - Guide (6750209, v3), sections 5-6; ADR-008 (8454170, v1).
"""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass, field
from typing import Any, Literal

SCHEMA_VERSION = "2"

Section = Literal[
    "catalog",
    "business-context",
    "business",
    "product",
    "technical",
    "decisions",
    "evidence",
    "knowledge-gaps",
    "industry-extensions",
]
SECTIONS: tuple[str, ...] = Section.__args__  # type: ignore[attr-defined]

State = Literal["draft", "validated", "archived"]
STATES: tuple[str, ...] = State.__args__  # type: ignore[attr-defined]

ArtifactClass = Literal[
    "textual",
    "editable_visual",
    "binary_asset",
    "work_item",
    "source_code",
    "external_reference",
]

# Fixed namespace so every deployment derives the same point IDs for the same input.
POINT_ID_NAMESPACE = uuid.uuid5(
    uuid.NAMESPACE_URL, "https://devsinsight.atlassian.net/wiki/spaces/AIEF/contract/v2"
)

# Fields a knowledge base item must carry; missing ones are reported, never invented.
REQUIRED_KB_FIELDS: tuple[str, ...] = ("key", "artifact_type", "section", "lifecycle.state")


@dataclass(frozen=True)
class Source:
    provider: str
    provider_artifact_id: str
    canonical_url: str
    version: str


@dataclass(frozen=True)
class Authority:
    artifact_class: ArtifactClass
    is_authoritative: bool = True
    owner: str | None = None


@dataclass(frozen=True)
class Lifecycle:
    state: State = "draft"
    valid_from: str | None = None
    valid_to: str | None = None


@dataclass(frozen=True)
class Relationship:
    type: str
    target_key: str


@dataclass(frozen=True)
class NormalizedKnowledgeArtifact:
    artifact_id: str
    title: str
    source: Source
    authority: Authority
    text: str
    key: str | None = None
    artifact_type: str | None = None
    section: Section | None = None
    lifecycle: Lifecycle = field(default_factory=Lifecycle)
    relationships: tuple[Relationship, ...] = ()
    classification: str = "internal"
    missing_fields: tuple[str, ...] = ()
    schema_version: str = SCHEMA_VERSION

    @property
    def metadata_complete(self) -> bool:
        return not self.missing_fields

    @property
    def content_hash(self) -> str:
        return content_hash(self.text)


def content_hash(text: str) -> str:
    """Hash of normalized text: line endings unified, trailing spaces and outer blank lines removed."""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    normalized = "\n".join(line.rstrip() for line in lines).strip("\n")
    return "sha256:" + hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def point_id(artifact_id: str, version: str, heading_path: tuple[str, ...], position: int) -> str:
    """Deterministic point ID: artifact, source version and chunk position (heading path + index).

    A new source version yields new IDs, so the previous version's points must be deleted.
    """
    if position < 0:
        raise ValueError("position must be >= 0")
    name = "\x1f".join([artifact_id, version, "\x1e".join(heading_path), str(position)])
    return str(uuid.uuid5(POINT_ID_NAMESPACE, name))


def normalize(
    *,
    artifact_id: str,
    title: str,
    source: Source,
    authority: Authority,
    text: str,
    key: str | None,
    artifact_type: str | None,
    section: str | None,
    state: str | None,
    archived_at_source: bool = False,
    relationships: tuple[Relationship, ...] = (),
    classification: str = "internal",
) -> NormalizedKnowledgeArtifact:
    """Build an artifact from the fields an adapter read, applying the framework's policies.

    - Never fabricate: a missing key, type or section stays missing and is listed.
    - A missing state becomes ``draft`` and is listed as missing.
    - An item archived at the source becomes ``archived``.
    - Unknown section or state values are treated as missing, not guessed.
    """
    missing: list[str] = []

    clean_key = key.strip() if key and key.strip() else None
    if clean_key is None:
        missing.append("key")

    clean_type = artifact_type.strip() if artifact_type and artifact_type.strip() else None
    if clean_type is None:
        missing.append("artifact_type")

    clean_section: Section | None = section if section in SECTIONS else None  # type: ignore[assignment]
    if clean_section is None:
        missing.append("section")

    if archived_at_source:
        clean_state: State = "archived"
    elif state in STATES:
        clean_state = state  # type: ignore[assignment]
    else:
        clean_state = "draft"
        missing.append("lifecycle.state")

    return NormalizedKnowledgeArtifact(
        artifact_id=artifact_id,
        title=title,
        source=source,
        authority=authority,
        text=text,
        key=clean_key,
        artifact_type=clean_type,
        section=clean_section,
        lifecycle=Lifecycle(state=clean_state),
        relationships=relationships,
        classification=classification,
        missing_fields=tuple(missing),
    )


@dataclass(frozen=True)
class Chunk:
    artifact: NormalizedKnowledgeArtifact
    heading_path: tuple[str, ...]
    position: int
    text: str

    @property
    def point_id(self) -> str:
        return point_id(
            self.artifact.artifact_id, self.artifact.source.version, self.heading_path, self.position
        )

    @property
    def content_hash(self) -> str:
        return content_hash(self.text)

    @property
    def embedding_text(self) -> str:
        """Text to embed: title and heading path as deterministic context, then the chunk."""
        context = " > ".join((self.artifact.title, *self.heading_path))
        return f"{context}\n\n{self.text}"

    def payload(self) -> dict[str, Any]:
        """Projection payload: contract fields plus chunk data. Never contains binaries."""
        a = self.artifact
        return {
            "schema_version": a.schema_version,
            "artifact_id": a.artifact_id,
            "key": a.key,
            "section": a.section,
            "artifact_type": a.artifact_type,
            "title": a.title,
            "lifecycle": {"state": a.lifecycle.state},
            "source": {
                "provider": a.source.provider,
                "provider_artifact_id": a.source.provider_artifact_id,
                "canonical_url": a.source.canonical_url,
                "version": a.source.version,
            },
            "authority": {
                "artifact_class": a.authority.artifact_class,
                "is_authoritative": a.authority.is_authoritative,
                "owner": a.authority.owner,
            },
            "permissions": {"classification": a.classification},
            "relationships": [{"type": r.type, "key": r.target_key} for r in a.relationships],
            "metadata_complete": a.metadata_complete,
            "missing_fields": list(a.missing_fields),
            "content_hash": self.content_hash,
            "heading_path": list(self.heading_path),
            "position": self.position,
            "text": self.text,
        }
