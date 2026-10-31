from types import SimpleNamespace

from app import ask


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(
        usage_metadata=SimpleNamespace(prompt_token_count=12, candidates_token_count=34),
        text="回答",
    )

    class FakeChat:
        def send_message(self, question):
            return response

    chat = FakeChat()

    assert ask.ask("質問", chat) == "回答"
    assert capsys.readouterr().out == "[usage] input_tokens=12, output_tokens=34\n"


def test_ask_sends_questions_to_the_same_chat(capsys):
    class FakeChat:
        def __init__(self):
            self.questions = []

        def send_message(self, question):
            self.questions.append(question)
            return SimpleNamespace(usage_metadata=None, text=f"{question}への回答")

    chat = FakeChat()

    assert ask.ask("最初の質問", chat) == "最初の質問への回答"
    assert ask.ask("続きの質問", chat) == "続きの質問への回答"
    assert chat.questions == ["最初の質問", "続きの質問"]