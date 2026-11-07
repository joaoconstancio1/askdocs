import numpy as np
import pytest

from askdocs.chunking import Chunk
from askdocs.embeddings import normalize
from askdocs.search import Index


class KeywordEmbedder:
    """Embedder falso para testes: um eixo por palavra-chave. Sem download de modelo."""

    KEYWORDS = ["falha", "token", "estado", "versão"]

    def embed(self, texts: list[str]) -> np.ndarray:
        rows = [[float(t.lower().count(k)) for k in self.KEYWORDS] for t in texts]
        return normalize(np.array(rows, dtype=np.float32) + 1e-6)


def make_index() -> Index:
    chunks = [
        Chunk("a.md", 0, "A taxa de falha passou de 1%, pausamos a liberação. Falha crítica."),
        Chunk("b.md", 0, "O token de acesso expira e o token de renovação é usado."),
        Chunk("c.md", 0, "Cada estado é imutável; emitimos um estado novo."),
    ]
    return Index(chunks, KeywordEmbedder())


def test_search_returns_most_similar_first():
    hits = make_index().search("o que fazer com falha?", k=3)
    assert hits[0].chunk.source == "a.md"
    assert hits[0].score >= hits[1].score >= hits[2].score


def test_search_respects_k():
    assert len(make_index().search("token", k=2)) == 2


def test_invalid_inputs():
    with pytest.raises(ValueError):
        Index([], KeywordEmbedder())
    with pytest.raises(ValueError):
        make_index().search("x", k=0)


def test_normalize_gives_unit_vectors():
    v = normalize(np.array([[3.0, 4.0], [0.0, 0.0]], dtype=np.float32))
    assert np.allclose(np.linalg.norm(v[0]), 1.0)
    assert np.allclose(v[1], 0.0)
