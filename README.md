# AskDocs

Assistente de perguntas e respostas sobre documentos, com RAG (busca nos documentos antes de responder) e avaliação da qualidade da busca.

Projeto de estudo em construção. Os documentos em `docs/` são exemplos fictícios escritos para este projeto.

## Etapas

- [x] 1. Divisão dos documentos em trechos (chunking), com testes
- [x] 2. Busca por significado (embeddings)
- [x] 3. Resposta com fontes (LLM opcional)
- [x] 4. API e avaliação da busca
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

## Avaliação da busca

`eval/questions.jsonl` tem 21 perguntas: 16 com resposta conhecida nos documentos e 5 sem resposta. O acerto conta quando o trecho recuperado contém a frase esperada.

```bash
.venv\Scripts\python -m askdocs.evaluate
```

Resultado da última execução (saída completa em `eval/results.txt`):

| Métrica | Valor |
|---|---|
| hit@1 (trecho certo em 1º) | 68,8% (11 de 16) |
| hit@3 (trecho certo entre os 3 primeiros) | 100% (16 de 16) |
| Sem resposta recusadas com limite 0,30 | 100% (5 de 5) |
| Com resposta mantidas com limite 0,30 | 94% (15 de 16) |

Limitações, para ler os números com cuidado:

- São apenas 3 documentos curtos e 21 perguntas, escritas pelo autor do projeto, não por usuários independentes.
- Os 0,30 foram escolhidos olhando este mesmo conjunto. A margem é pequena: a menor pontuação de uma pergunta com resposta (0,293) é quase igual à maior de uma sem resposta (0,298).
- Os números mostram que a busca funciona neste exemplo, não que generaliza para outros documentos.

## API

```bash
.venv\Scripts\python -m pip install -e ".[api]"
.venv\Scripts\python -m uvicorn askdocs.api:app
```

- `GET /health` retorna `{"status": "ok"}`.
- `POST /ask` com `{"question": "...", "k": 3}` retorna `{"answer": "...", "sources": ["[1] arquivo.md (trecho N)"]}`.
- Documentação interativa em `http://127.0.0.1:8000/docs`.
