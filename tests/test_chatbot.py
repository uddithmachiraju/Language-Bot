import re
import os
import sys
import pytest
import unicodedata
from unittest.mock import patch 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.chatbot import Language_Bot

# Normalize text function (unchanged)
def normalize_text(text):
    text = unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("utf-8").lower()
    text = re.sub(r'\s+([?.!,])', r'\1', text)  # Remove space before punctuation
    return text.strip()

@pytest.fixture
def chatbot():
    """Fixture to create a chatbot instance quickly."""
    return Language_Bot(
        user_id="test_user",
        known_language="English",
        target_language="French",
        proficiency="Beginner",
        use_openai=False  # Mock model, so no OpenAI calls
    )


@patch.object(Language_Bot, "detect_mistakes", return_value="Bonjour, comment ça va ?")
@patch.object(Language_Bot, "chat", return_value="Bonjour, comment ça va ?")
def test_chat_response(mock_chat, mock_detect_mistakes, chatbot):
    user_input = "Bonjour, comment tu vas ?"
    response = chatbot.chat(user_input)

    assert normalize_text(response) == normalize_text("Bonjour, comment ça va ?"), "Chatbot response incorrect"

@patch.object(Language_Bot, "detect_mistakes", return_value="Bonjour, comment ça va ?")
def test_detect_mistakes(mock_detect_mistakes, chatbot):
    user_input = "Bonjour, comment tu vas ?"
    corrected_text = chatbot.detect_mistakes(user_input)

    assert normalize_text(corrected_text) == normalize_text("Bonjour, comment ça va ?"), "Mistake detection failed"

@patch("src.chatbot.log_mistakes")  # Avoids real DB or file writes
@patch.object(Language_Bot, "detect_mistakes", return_value="Bonjour, comment ça va ?")
def test_log_mistakes(mock_detect_mistakes, mock_log_mistakes, chatbot):
    user_input = "Bonjour, comment tu vas ?"
    chatbot.chat(user_input)

    mock_log_mistakes.assert_called_once_with(
        chatbot.user_id, user_input, "Bonjour, comment ça va ?"
    )

@patch("src.chatbot.openai.ChatCompletion.create", return_value={"choices": [{"message": {"content": "Bonjour, comment ça va ?"}}]})
def test_openai_mistake_detection(mock_openai):
    chatbot = Language_Bot("test_user", "English", "French", "Beginner", use_openai=True)

    user_input = "Bonjour, comment tu vas ?"
    corrected_text = chatbot.detect_mistakes(user_input)

    assert normalize_text(corrected_text) == normalize_text("Bonjour, comment ça va ?"), "OpenAI mistake detection failed"
