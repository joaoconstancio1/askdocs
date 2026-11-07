# AskDocs

Assistente de perguntas e respostas sobre documentos, com RAG (busca nos documentos antes de responder) e avaliação da qualidade da busca.

Projeto de estudo em construção. Os documentos em `docs/` são exemplos fictícios escritos para este projeto.

## Etapas

- [x] 1. Divisão dos documentos em trechos (chunking), com testes
- [x] 2. Busca por significado (embeddings)
- [x] 3. Resposta com fontes (LLM opcional)
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

## Perguntar com fontes

```bash
.venv\Scripts\python -m askdocs.ask "quando devo pausar a liberação gradual?"
```

- **Sem chave de API:** mostra os trechos mais relevantes, cada um com a fonte.
- **Com chave:** copie `.env.example` para `.env`, preencha `ANTHROPIC_API_KEY` e instale `pip install -e ".[llm]"`. O modelo recebe apenas os trechos encontrados e é instruído a responder só com eles, citando as fontes.
- Se nenhum trecho passa do limite de similaridade (`DEFAULT_MIN_SCORE`), a resposta é "Não encontrei isso nos documentos.". O limite atual (0,30) é provisório e será calibrado na avaliação.

Status: o caminho com LLM foi testado apenas com um cliente simulado nos testes; ainda não foi executado contra a API real.
