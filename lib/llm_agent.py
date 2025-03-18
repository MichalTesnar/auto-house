import json
from google import genai

class LLMAgent():
    def __init__(self):
        with open('secret/aistudio_credentials.json') as f:
            data = json.load(f)
            self.client = genai.Client(api_key=data["KEY"])
            self.model = "gemini-2.0-flash"

    def respond(self, message: str):
        response = self.client.models.generate_content(model=self.model, contents=message)
        return response.text