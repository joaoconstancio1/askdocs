"""Índice de busca por similaridade de significado."""

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from askdocs.chunking import Chunk, load_chunks
from askdocs.embeddings import Embedder


@dataclass(frozen=True)
class Hit:
    chunk: Chunk
    score: float


class Index:
    """Guarda os trechos e seus vetores e devolve os mais parecidos com a pergunta."""

    def __init__(self, chunks: list[Chunk], embedder: Embedder):
        if not chunks:
            raise ValueError("o índice precisa de pelo menos um trecho")
        self._chunks = chunks
        self._embedder = embedder
        self._vectors = embedder.embed([c.text for c in chunks])

    @classmethod
    def from_folder(cls, folder: Path, embedder: Embedder, **chunk_args) -> "Index":
        return cls(load_chunks(folder, **chunk_args), embedder)

    def search(self, query: str, k: int = 3) -> list[Hit]:
        if k <= 0:
            raise ValueError("k deve ser maior que zero")
        query_vector = self._embedder.embed([query])[0]
        # Vetores normalizados: produto escalar equivale à similaridade de cosseno.
        scores = self._vectors @ query_vector
        order = np.argsort(-scores)[:k]
        return [Hit(self._chunks[i], float(scores[i])) for i in order]


def main() -> None:
    import argparse

    from askdocs.embeddings import FastEmbedder

    parser = argparse.ArgumentParser(description="Busca por significado nos documentos")
    parser.add_argument("query")
    parser.add_argument("--docs", default="docs")
    parser.add_argument("-k", type=int, default=3)
    args = parser.parse_args()

    index = Index.from_folder(Path(args.docs), FastEmbedder())
    for hit in index.search(args.query, args.k):
        print(f"\n[{hit.score:.3f}] {hit.chunk.source} (trecho {hit.chunk.index})")
        print(hit.chunk.text)


if __name__ == "__main__":
    main()
