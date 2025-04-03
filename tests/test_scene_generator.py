import sys 
import os 
import pytest
from unittest.mock import patch
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.scene_generator import SceneGenerator

@pytest.fixture
def scene_generator():
    """Fixture to create a SceneGenerator instance using Hugging Face."""
    return SceneGenerator(target_language="Spanish", proficiency="Intermediate")

@patch("src.scene_generator.free_model")
def test_generate_scene(mock_huggingface, scene_generator):
    """
    Tests scene generation using Hugging Face model.
    """
    # ✅ Mock the return value correctly as a list, not a function
    mock_huggingface.return_value = [
        {"generated_text": "You are at a Spanish market buying fruits."}
    ]

    # ✅ Ensure the instance uses the mocked model
    scene_generator.model = mock_huggingface

    # ✅ Call the function and assert expected output
    scenario = scene_generator.generate_scene()

    assert isinstance(scenario, str), "Output should be a string"
    assert len(scenario) > 10, "Scenario should not be empty"
    assert "market" in scenario.lower(), "Scenario content is incorrect"