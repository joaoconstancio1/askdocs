# AskDocs

Assistente de perguntas e respostas sobre documentos, com RAG (busca nos documentos antes de responder) e avaliação da qualidade da busca.

Projeto de estudo em construção. Os documentos em `docs/` são exemplos fictícios escritos para este projeto.

## Etapas

- [x] 1. Divisão dos documentos em trechos (chunking), com testes
- [x] 2. Busca por significado (embeddings)
- [ ] 3. Resposta com fontes (LLM opcional)
- [ ] 4. API e avaliação da busca
- [ ] 5. Docker e CI

## Rodar os testes

```bash
python -m venv .venv
.venv\Scripts\python -m pip install pytest
.venv\Scripts\python -m pytest
```

## Buscar nos documentos

```bash
.venv\Scripts\python -m pip install -e .
.venv\Scripts\python -m askdocs.search "quando devo pausar a liberação gradual?"
```

No primeiro uso, o modelo multilíngue `paraphrase-multilingual-MiniLM-L12-v2` (cerca de 220 MB) é baixado automaticamente.
