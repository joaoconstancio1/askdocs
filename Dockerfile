FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    ASKDOCS_DOCS=/app/docs \
    HF_HOME=/app/.cache

WORKDIR /app

# Instala as dependências antes do código, para aproveitar o cache de camadas.
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install ".[api]"

COPY docs ./docs

# Baixa o modelo de busca durante a construção, para a primeira pergunta não demorar.
RUN python -c "from askdocs.embeddings import FastEmbedder; FastEmbedder()"

# Roda sem privilégios de administrador.
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=40s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"

CMD ["uvicorn", "askdocs.api:app", "--host", "0.0.0.0", "--port", "8000"]
