from types import SimpleNamespace
from unittest.mock import patch

from app.ask import ask


def test_ask_prints_token_usage(capsys):
    response = SimpleNamespace(
        text="回答",
        usage_metadata=SimpleNamespace(prompt_token_count=12, candidates_token_count=8),
    )
    calls = []

    def generate_content(**kwargs):
        calls.append(kwargs)
        return response

    client = SimpleNamespace(models=SimpleNamespace(generate_content=generate_content))

    with patch("app.ask.genai.Client", return_value=client), patch("app.ask.get_api_key", return_value="key"):
        assert ask("質問", temperature=0.2) == "回答"

    output = capsys.readouterr().out
    assert "input_tokens=12" in output
    assert "output_tokens=8" in output
    assert calls[0]["config"].temperature == 0.2


def test_ask_does_not_fail_when_token_usage_is_missing(capsys):
    response = SimpleNamespace(text="回答", usage_metadata=None)
    client = SimpleNamespace(models=SimpleNamespace(generate_content=lambda **kwargs: response))

    with patch("app.ask.genai.Client", return_value=client), patch("app.ask.get_api_key", return_value="key"):
        assert ask("質問") == "回答"

    output = capsys.readouterr().out
    assert "input_tokens=N/A" in output
    assert "output_tokens=N/A" in output