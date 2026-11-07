"""Mede a qualidade da busca com perguntas de resposta conhecida.

Para cada pergunta com resposta ("expected"), o acerto é: o trecho recuperado
contém a frase esperada. Medimos:
  - hit@1: o trecho certo é o primeiro resultado
  - hit@k: o trecho certo está entre os k primeiros
Perguntas com "expected": null não têm resposta nos documentos; usamos o maior
score delas para escolher o limite de relevância (abaixo dele, o sistema
responde "não encontrei").
"""

import json
from dataclasses import dataclass
from pathlib import Path

from askdocs.search import Index


@dataclass(frozen=True)
class Case:
    question: str
    expected: str | None


def load_cases(path: Path) -> list[Case]:
    cases = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            cases.append(Case(row["question"], row["expected"]))
    return cases


def contains(text: str, phrase: str) -> bool:
    return phrase.lower() in text.lower()


def evaluate(index: Index, cases: list[Case], k: int = 3) -> dict:
    answerable = [c for c in cases if c.expected]
    unanswerable = [c for c in cases if not c.expected]

    hit1 = hitk = 0
    answerable_top_scores: list[float] = []
    misses: list[str] = []
    for case in answerable:
        hits = index.search(case.question, k)
        answerable_top_scores.append(hits[0].score)
        if contains(hits[0].chunk.text, case.expected):
            hit1 += 1
        if any(contains(h.chunk.text, case.expected) for h in hits):
            hitk += 1
        else:
            misses.append(case.question)

    unanswerable_top_scores = [index.search(c.question, 1)[0].score for c in unanswerable]

    return {
        "k": k,
        "answerable": len(answerable),
        "unanswerable": len(unanswerable),
        "hit_at_1": hit1 / len(answerable) if answerable else 0.0,
        "hit_at_k": hitk / len(answerable) if answerable else 0.0,
        "misses": misses,
        "answerable_top_scores": answerable_top_scores,
        "unanswerable_top_scores": unanswerable_top_scores,
    }


def threshold_sweep(result: dict, thresholds: list[float]) -> list[dict]:
    """Para cada limite: quantas perguntas respondíveis seguem ativas e quantas
    sem resposta são corretamente recusadas."""
    rows = []
    a, u = result["answerable_top_scores"], result["unanswerable_top_scores"]
    for t in thresholds:
        rows.append(
            {
                "threshold": t,
                "answerable_kept": sum(s >= t for s in a) / len(a) if a else 0.0,
                "unanswerable_rejected": sum(s < t for s in u) / len(u) if u else 0.0,
            }
        )
    return rows


def main() -> None:
    import argparse

    from askdocs.embeddings import FastEmbedder

    parser = argparse.ArgumentParser(description="Avalia a busca do AskDocs")
    parser.add_argument("--docs", default="docs")
    parser.add_argument("--cases", default="eval/questions.jsonl")
    parser.add_argument("-k", type=int, default=3)
    args = parser.parse_args()

    index = Index.from_folder(Path(args.docs), FastEmbedder())
    result = evaluate(index, load_cases(Path(args.cases)), args.k)

    print(f"Perguntas com resposta: {result['answerable']} | sem resposta: {result['unanswerable']}")
    print(f"hit@1: {result['hit_at_1']:.1%}")
    print(f"hit@{result['k']}: {result['hit_at_k']:.1%}")
    if result["misses"]:
        print("Erros (fora do top-k):")
        for q in result["misses"]:
            print(f"  - {q}")
    a, u = result["answerable_top_scores"], result["unanswerable_top_scores"]
    print(f"Score do 1º resultado, com resposta: mín {min(a):.3f}, máx {max(a):.3f}")
    print(f"Score do 1º resultado, sem resposta: mín {min(u):.3f}, máx {max(u):.3f}")
    print("\nlimite | com resposta mantidas | sem resposta recusadas")
    for row in threshold_sweep(result, [0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]):
        print(f"{row['threshold']:.2f}   | {row['answerable_kept']:.0%}                  | {row['unanswerable_rejected']:.0%}")


if __name__ == "__main__":
    main()
