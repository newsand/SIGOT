import google.generativeai as genai
import os
from dotenv import load_dotenv
# Load environment variables from .env file
class GeminiConnector:
    def __init__(self, model_name, api_key=None):
        self.model_name = model_name
        if not api_key:
            load_dotenv()
            self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
            if not self.api_key:
                raise ValueError("Google API Key is required. Set it in the environment or provide it as an argument.")

        self.api_key = api_key


    def send_prompt(self, prompt: str):
        """Sends a prompt to the specified Gemini model and returns the generated text."""
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(model_name=self.model_name)

        try:
            response = model.generate_content([prompt, ""])
            return response.text
        except Exception as e:
            # Handle exceptions more gracefully, log errors, or return specific messages
            print(f"An error occurred: {e}")
            return None


# Example Usage:

# connector = GeminiConnector(model_name="gemini-1.5-flash")
# poem = connector.send_prompt("Write a short poem about the beauty of nature.")
# print(poem)
