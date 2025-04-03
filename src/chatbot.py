import openai
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from transformers import pipeline
from src.database import log_mistakes
# from src.config import OPENAI_API_KEY 

# # Uncomment if using OpenAI API
# openai.api_key = OPENAI_API_KEY

# Use a Free Model (Hugging Face Transformer)
free_model = pipeline("text-generation", model="distilgpt2", max_new_tokens = 50)

class Language_Bot:
    def __init__(self, user_id, known_language, target_language, proficiency, use_openai=False):
        """Initialize the chatbot with user details."""
        self.user_id = user_id
        self.known_language = known_language
        self.target_language = target_language
        self.proficiency = proficiency
        self.history = []
        self.use_openai = use_openai  # Switch between OpenAI and Hugging Face models 

        if use_openai:
            self.model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        else:
            self.model = free_model

    def detect_mistakes(self, user_input):
        """Uses AI model to analyze and correct mistakes."""
        correction_prompt = f"""
        Identify and correct grammar, vocabulary, or sentence structure mistakes
        in this {self.target_language} sentence. Provide the corrected version only: "{user_input}"
        """
        
        if self.use_openai:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Grammar correction assistant"},
                    {"role": "user", "content": correction_prompt}
                ]
            )
            return response["choices"][0]["message"]["content"].strip()
        else:
            response = self.model(correction_prompt, max_length=100, do_sample=True)[0]["generated_text"]
            return response.strip() 

    def generate_prompt(self, user_input):
        """Creates a prompt for the AI model to respond appropriately."""
        system_message = f"""
        You are a language tutor helping a student learn {self.target_language}. 
        The user speaks {self.known_language} and has {self.proficiency} proficiency in {self.target_language}.
        Your task is to respond in {self.target_language}, correct mistakes, and provide brief explanations.
        """
        messages = [SystemMessage(content=system_message)] + self.history
        messages.append(HumanMessage(content=user_input))
        return messages

    def chat(self, user_input):
        """Processes user input, detects mistakes, provides corrections, and generates a response."""
        corrected_text = self.detect_mistakes(user_input)

        # Log only if there is a mistake
        if corrected_text != user_input:
            log_mistakes(self.user_id, user_input, corrected_text)

        prompt_message = self.generate_prompt(corrected_text)

        if self.use_openai:
            response = self.model.invoke(prompt_message)
            response_text = response.content
        else:
            response_text = self.model(prompt_message[-1].content, max_length=150, do_sample=True)[0]["generated_text"]

        # Store conversation history
        self.history.append(HumanMessage(content=user_input))
        self.history.append(AIMessage(content=response_text))

        return response_text
