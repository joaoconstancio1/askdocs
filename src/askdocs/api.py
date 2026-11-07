"""API HTTP do AskDocs (FastAPI).

Rodar:  uvicorn askdocs.api:app --reload
Docs interativas: http://127.0.0.1:8000/docs
"""

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from askdocs.answer import Answerer, make_answerer
from askdocs.config import load_dotenv
from askdocs.search import Index


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)
    k: int = Field(default=3, ge=1, le=10)


class AskResponse(BaseModel):
    answer: str
    sources: list[str]


def create_app(index: Index | None = None, answerer: Answerer | None = None) -> FastAPI:
    """Fábrica da aplicação. Index e answerer podem ser injetados (testes)."""
    app = FastAPI(title="AskDocs", version="0.1.0")
    state: dict = {"index": index, "answerer": answerer}

    def get_state() -> tuple[Index, Answerer]:
        # Criação tardia: o modelo só é carregado na primeira pergunta.
        if state["index"] is None:
            from askdocs.embeddings import FastEmbedder

            load_dotenv()
            docs = Path(os.environ.get("ASKDOCS_DOCS", "docs"))
            state["index"] = Index.from_folder(docs, FastEmbedder())
        if state["answerer"] is None:
            state["answerer"] = make_answerer()
        return state["index"], state["answerer"]

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    @app.post("/ask", response_model=AskResponse)
    def ask(body: AskRequest) -> AskResponse:
        question = body.question.strip()
        if not question:
            raise HTTPException(status_code=422, detail="a pergunta não pode ser vazia")
        idx, ans = get_state()
        result = ans.answer(question, idx.search(question, body.k))
        return AskResponse(answer=result.text, sources=result.sources)

    return app


app = create_app()
