from askdocs.chunking import Chunk
from askdocs.evaluate import Case, evaluate, threshold_sweep
from askdocs.search import Index
from tests.test_search import KeywordEmbedder


def make_index() -> Index:
    return Index(
        [
            Chunk("a.md", 0, "A taxa de falha passou de 1%, pausamos a liberação. Falha crítica."),
            Chunk("b.md", 0, "O token de acesso expira e o token de renovação é usado."),
        ],
        KeywordEmbedder(),
    )


def test_evaluate_counts_hits_and_scores():
    cases = [
        Case("o que fazer com falha?", "taxa de falha"),
        Case("como funciona o token?", "token de renovação"),
        Case("qual a receita do bolo?", None),
    ]
    result = evaluate(make_index(), cases, k=1)
    assert result["answerable"] == 2 and result["unanswerable"] == 1
    assert result["hit_at_1"] == 1.0 and result["hit_at_k"] == 1.0
    assert len(result["unanswerable_top_scores"]) == 1


def test_threshold_sweep_is_monotonic():
    result = {"answerable_top_scores": [0.9, 0.5], "unanswerable_top_scores": [0.2, 0.4]}
    rows = threshold_sweep(result, [0.1, 0.45, 0.95])
    assert [r["answerable_kept"] for r in rows] == [1.0, 1.0, 0.0]
    assert [r["unanswerable_rejected"] for r in rows] == [0.0, 1.0, 1.0]
