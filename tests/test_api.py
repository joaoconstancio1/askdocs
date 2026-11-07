from fastapi.testclient import TestClient

from askdocs.answer import ExtractiveAnswerer
from askdocs.api import create_app
from askdocs.chunking import Chunk
from askdocs.search import Index
from tests.test_search import KeywordEmbedder


def client() -> TestClient:
    chunks = [
        Chunk("a.md", 0, "A taxa de falha passou de 1%, pausamos a liberação. Falha crítica."),
        Chunk("b.md", 0, "O token de acesso expira e o token de renovação é usado."),
    ]
    index = Index(chunks, KeywordEmbedder())
    return TestClient(create_app(index, ExtractiveAnswerer(min_score=0.5)))


def test_health():
    assert client().get("/health").json() == {"status": "ok"}


def test_ask_returns_answer_with_sources():
    response = client().post("/ask", json={"question": "o que fazer com falha?", "k": 1})
    assert response.status_code == 200
    body = response.json()
    assert "taxa de falha" in body["answer"]
    assert body["sources"] == ["[1] a.md (trecho 0)"]


def test_ask_validates_input():
    c = client()
    assert c.post("/ask", json={"question": ""}).status_code == 422
    assert c.post("/ask", json={"question": "x", "k": 0}).status_code == 422
    assert c.post("/ask", json={"question": "   "}).status_code == 422
