"""Divide documentos em trechos (chunks) para a busca.

Um modelo de busca compara o significado da pergunta com trechos curtos.
Trechos grandes demais misturam assuntos; pequenos demais perdem contexto.
Aqui juntamos parágrafos inteiros até um limite de caracteres e repetimos o
final de cada trecho no início do próximo (sobreposição), para não cortar uma
ideia exatamente na fronteira.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Chunk:
    source: str
    index: int
    text: str


def split_paragraphs(text: str) -> list[str]:
    return [p.strip() for p in text.split("\n\n") if p.strip()]


def chunk_text(text: str, max_chars: int = 500, overlap: int = 100) -> list[str]:
    if max_chars <= 0:
        raise ValueError("max_chars deve ser maior que zero")
    if not 0 <= overlap < max_chars:
        raise ValueError("overlap deve estar entre 0 e max_chars - 1")

    chunks: list[str] = []
    current = ""
    for paragraph in split_paragraphs(text):
        # Parágrafo maior que o limite: corta em janelas com sobreposição.
        while len(paragraph) > max_chars:
            if current:
                chunks.append(current)
                current = ""
            chunks.append(paragraph[:max_chars])
            paragraph = paragraph[max_chars - overlap :]
        candidate = f"{current}\n\n{paragraph}" if current else paragraph
        if len(candidate) <= max_chars:
            current = candidate
        else:
            chunks.append(current)
            tail = current[-overlap:] if overlap else ""
            current = f"{tail}\n\n{paragraph}".strip() if tail else paragraph
            if len(current) > max_chars:
                current = paragraph
    if current:
        chunks.append(current)
    return chunks


def load_chunks(folder: Path, max_chars: int = 500, overlap: int = 100) -> list[Chunk]:
    result: list[Chunk] = []
    for path in sorted(Path(folder).glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for i, piece in enumerate(chunk_text(text, max_chars, overlap)):
            result.append(Chunk(source=path.name, index=i, text=piece))
    return result
