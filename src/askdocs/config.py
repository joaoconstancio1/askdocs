"""Carrega variáveis de um arquivo .env local (sem dependências extras)."""

import os
from pathlib import Path


def load_dotenv(path: Path = Path(".env")) -> None:
    """Lê linhas CHAVE=valor. Não sobrescreve variáveis já definidas no ambiente."""
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
