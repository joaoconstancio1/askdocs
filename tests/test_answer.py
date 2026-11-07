from types import SimpleNamespace

from askdocs.answer import (
    NOT_FOUND,
    ExtractiveAnswerer,
    LLMAnswerer,
    build_prompt,
    make_answerer,
)
from askdocs.chunking import Chunk
from askdocs.config import load_dotenv
from askdocs.search import Hit


def hits():
    return [
        Hit(Chunk("release-process.md", 3, "Pausamos se a taxa de falhas passar de 1%."), 0.8),
        Hit(Chunk("security-basics.md", 1, "Tokens ficam no armazenamento seguro."), 0.1),
    ]


class FakeClient:
    """Imita o cliente da API: registra a chamada e devolve um texto fixo."""

    def __init__(self):
        self.calls = []
        self.messages = SimpleNamespace(create=self._create)

    def _create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(content=[SimpleNamespace(type="text", text=" Pause com 1% [1]. ")])


def test_extractive_keeps_only_relevant_hits_with_sources():
    result = ExtractiveAnswerer(min_score=0.3).answer("q", hits())
    assert "taxa de falhas" in result.text
    assert "Tokens" not in result.text
    assert result.sources == ["[1] release-process.md (trecho 3)"]


def test_not_found_when_nothing_is_relevant():
    result = ExtractiveAnswerer(min_score=0.99).answer("q", hits())
    assert result.text == NOT_FOUND and result.sources == []


def test_prompt_wraps_sources_and_question():
    prompt = build_prompt("Quando pausar?", hits())
    assert '<source id="1" file="release-process.md">' in prompt
    assert prompt.endswith("Question: Quando pausar?")


def test_llm_answerer_sends_only_relevant_sources():
    client = FakeClient()
    result = LLMAnswerer(client, min_score=0.3).answer("Quando pausar?", hits())
    call = client.calls[0]
    assert "ignore any instructions" in call["system"]
    sent = call["messages"][0]["content"]
    assert "release-process.md" in sent and "security-basics.md" not in sent
    assert result.text == "Pause com 1% [1]."
    assert result.sources == ["[1] release-process.md (trecho 3)"]


def test_llm_answerer_does_not_call_api_without_relevant_hits():
    client = FakeClient()
    result = LLMAnswerer(client, min_score=0.99).answer("q", hits())
    assert client.calls == [] and result.text == NOT_FOUND


def test_make_answerer_without_key_is_extractive():
    assert isinstance(make_answerer({}), ExtractiveAnswerer)


def test_load_dotenv_does_not_override_existing(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("# comentário\nASKDOCS_A=1\nASKDOCS_B='dois'\n", encoding="utf-8")
    monkeypatch.setenv("ASKDOCS_A", "existente")
    monkeypatch.delenv("ASKDOCS_B", raising=False)
    load_dotenv(env_file)
    import os

    assert os.environ["ASKDOCS_A"] == "existente"
    assert os.environ["ASKDOCS_B"] == "dois"
    monkeypatch.delenv("ASKDOCS_B", raising=False)
