"""Tests for contract.py. Copy them next to the module (for example packages/core/tests/)."""

from __future__ import annotations

import uuid

import pytest

from contract import (
    Authority,
    Chunk,
    Relationship,
    Source,
    content_hash,
    normalize,
    point_id,
)

SOURCE = Source("confluence", "12345", "https://example.atlassian.net/wiki/pages/12345", "7")
AUTHORITY = Authority("textual", owner="product-owner")


def make(**overrides):
    fields = dict(
        artifact_id="confluence:12345",
        title="Checkout Payment",
        source=SOURCE,
        authority=AUTHORITY,
        text="Body",
        key="feature-checkout-payment",
        artifact_type="feature",
        section="product",
        state="validated",
    )
    fields.update(overrides)
    return normalize(**fields)


def test_complete_metadata_is_kept():
    a = make()
    assert a.metadata_complete
    assert a.lifecycle.state == "validated"
    assert a.key == "feature-checkout-payment"


def test_missing_state_becomes_draft_and_is_reported():
    a = make(state=None)
    assert a.lifecycle.state == "draft"
    assert "lifecycle.state" in a.missing_fields
    assert not a.metadata_complete


def test_missing_key_is_never_invented():
    a = make(key="  ")
    assert a.key is None
    assert "key" in a.missing_fields


def test_unknown_section_and_state_are_not_guessed():
    a = make(section="Product Area", state="approved")
    assert a.section is None
    assert a.lifecycle.state == "draft"
    assert {"section", "lifecycle.state"} <= set(a.missing_fields)


def test_archived_at_source_wins():
    a = make(state="validated", archived_at_source=True)
    assert a.lifecycle.state == "archived"


def test_point_id_is_deterministic_uuid():
    first = point_id("confluence:12345", "7", ("Rules", "Refunds"), 0)
    second = point_id("confluence:12345", "7", ("Rules", "Refunds"), 0)
    assert first == second
    assert uuid.UUID(first).version == 5


def test_point_id_changes_with_version_and_position():
    base = point_id("confluence:12345", "7", ("Rules",), 0)
    assert point_id("confluence:12345", "8", ("Rules",), 0) != base
    assert point_id("confluence:12345", "7", ("Rules",), 1) != base
    assert point_id("confluence:12345", "7", ("Other",), 0) != base


def test_heading_path_levels_are_distinguished():
    assert point_id("a", "1", ("x y",), 0) != point_id("a", "1", ("x", "y"), 0)
    assert point_id("a", "1", ("x", "y"), 0) != point_id("a", "1", ("y", "x"), 0)


def test_point_id_rejects_negative_position():
    with pytest.raises(ValueError):
        point_id("a", "1", (), -1)


def test_content_hash_ignores_line_endings_and_trailing_spaces():
    assert content_hash("a  \r\nb\r\n") == content_hash("a\nb")
    assert content_hash("a\nb") != content_hash("a\nc")
    assert content_hash("x").startswith("sha256:")


def test_chunk_payload_carries_contract_fields_and_no_binaries():
    a = make(relationships=(Relationship("related", "capability-payments"),))
    chunk = Chunk(a, ("Business Rules", "Refunds"), 2, "Refunds within 30 days.")
    payload = chunk.payload()
    assert payload["key"] == "feature-checkout-payment"
    assert payload["source"] == {
        "provider": "confluence",
        "provider_artifact_id": "12345",
        "canonical_url": "https://example.atlassian.net/wiki/pages/12345",
        "version": "7",
    }
    assert payload["lifecycle"] == {"state": "validated"}
    assert payload["relationships"] == [{"type": "related", "key": "capability-payments"}]
    assert payload["metadata_complete"] is True
    assert payload["content_hash"] == content_hash("Refunds within 30 days.")
    assert all(not isinstance(v, (bytes, bytearray)) for v in payload.values())


def test_embedding_text_prefixes_title_and_heading_path():
    chunk = Chunk(make(), ("Business Rules", "Refunds"), 0, "Refunds within 30 days.")
    assert chunk.embedding_text.startswith("Checkout Payment > Business Rules > Refunds\n\n")


def test_new_version_changes_point_ids_but_not_content_hash():
    v7 = Chunk(make(), ("Rules",), 0, "Same text")
    v8 = Chunk(
        make(source=Source("confluence", "12345", SOURCE.canonical_url, "8")), ("Rules",), 0, "Same text"
    )
    assert v7.point_id != v8.point_id
    assert v7.content_hash == v8.content_hash  # embedding can be reused from the cache
