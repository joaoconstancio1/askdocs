"""Transforma textos em vetores (embeddings).

Um embedding é uma lista de números que representa o *significado* de um
texto. Textos com significado parecido ficam com vetores parecidos, mesmo sem
usar as mesmas palavras. É isso que permite buscar por sentido.
"""

from typing import Protocol

import numpy as np

DEFAULT_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


class Embedder(Protocol):
    def embed(self, texts: list[str]) -> np.ndarray:
        """Retorna uma matriz (len(texts), dimensão) com vetores normalizados."""


class FastEmbedder:
    """Embedder local (CPU) baseado em fastembed/ONNX. Baixa o modelo no primeiro uso."""

    def __init__(self, model_name: str = DEFAULT_MODEL):
        from fastembed import TextEmbedding  # import tardio: só carrega se usado

        self._model = TextEmbedding(model_name=model_name)

    def embed(self, texts: list[str]) -> np.ndarray:
        vectors = np.array(list(self._model.embed(texts)), dtype=np.float32)
        return normalize(vectors)


def normalize(vectors: np.ndarray) -> np.ndarray:
    """Deixa cada vetor com tamanho 1, para que produto escalar = similaridade de cosseno."""
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return vectors / norms
