from pathlib import Path

import pytest

from askdocs.chunking import chunk_text, load_chunks


def test_short_text_is_a_single_chunk():
    assert chunk_text("Olá mundo.", max_chars=100, overlap=10) == ["Olá mundo."]


def test_chunks_respect_max_chars():
    text = "\n\n".join(f"Parágrafo número {i} com algum texto." for i in range(30))
    chunks = chunk_text(text, max_chars=120, overlap=20)
    assert len(chunks) > 1
    assert all(len(c) <= 120 for c in chunks)


def test_no_content_is_lost():
    paragraphs = [f"Frase única {i}." for i in range(20)]
    chunks = chunk_text("\n\n".join(paragraphs), max_chars=80, overlap=10)
    joined = "\n".join(chunks)
    assert all(p in joined for p in paragraphs)


def test_long_paragraph_is_split_with_overlap():
    chunks = chunk_text("a" * 250, max_chars=100, overlap=20)
    assert len(chunks) >= 3
    assert all(len(c) <= 100 for c in chunks)


def test_invalid_arguments():
    with pytest.raises(ValueError):
        chunk_text("x", max_chars=0)
    with pytest.raises(ValueError):
        chunk_text("x", max_chars=10, overlap=10)


def test_load_chunks_reads_sample_docs():
    docs = Path(__file__).resolve().parent.parent / "docs"
    chunks = load_chunks(docs)
    sources = {c.source for c in chunks}
    assert {"release-process.md", "state-management.md", "security-basics.md"} <= sources
    assert all(c.text for c in chunks)
