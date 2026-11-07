"""Linha de comando: pergunta -> busca -> resposta com fontes."""

import argparse
from pathlib import Path

from askdocs.answer import make_answerer
from askdocs.config import load_dotenv
from askdocs.embeddings import FastEmbedder
from askdocs.search import Index


def main() -> None:
    parser = argparse.ArgumentParser(description="Pergunte aos seus documentos")
    parser.add_argument("question")
    parser.add_argument("--docs", default="docs")
    parser.add_argument("-k", type=int, default=3, help="quantos trechos buscar")
    args = parser.parse_args()

    load_dotenv()
    index = Index.from_folder(Path(args.docs), FastEmbedder())
    answerer = make_answerer()
    result = answerer.answer(args.question, index.search(args.question, args.k))

    print(result.text)
    if result.sources:
        print("\nFontes:")
        for source in result.sources:
            print(f"  {source}")


if __name__ == "__main__":
    main()
