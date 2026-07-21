import os
from dotenv import load_dotenv
from google import genai

# Load API key from .env file
load_dotenv()
api_key = os.getenv("API_KEY")

# Initialize client with API key from .env
client = genai.Client(api_key=api_key)

class Response:
    def generate_response(self, story_prompt: str):
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=story_prompt,
        )

        return response.text