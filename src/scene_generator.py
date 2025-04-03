from transformers import pipeline

# Load the Hugging Face model
free_model = pipeline("text-generation", model="distilgpt2", max_new_tokens=100)

class SceneGenerator:
    def __init__(self, target_language, proficiency):
        """
        Initializes the scene generator with Hugging Face model.
        """
        self.target_language = target_language
        self.proficiency = proficiency
        self.model = free_model

    def generate_scene(self):
        """
        Generates a practice scenario based on the user's target language and proficiency.
        """
        prompt = f"""
        Create a real-world practice scenario for a learner of {self.target_language}.
        The user is at a {self.proficiency} level. The scene should be engaging, 
        culturally relevant, and encourage conversation.
        """

        response = self.model(prompt, max_length=150, do_sample=True)[0]["generated_text"]
        return response.strip()