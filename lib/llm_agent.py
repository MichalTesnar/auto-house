import json
from google import genai

class LLMAgent():
    def __init__(self):
        
        self.system_prompt = "You are an online bot writing responses for me to offers about housing. You will receive my description, and you will receive description about the house in HTML format. Using relevant information, compile an email to the person offering the house introducing me and expressing interest in the offer in an approapriate language. Use any keywords they say you should mention. Do not provide any other description or explanation around this message, just the message itself. Do not include subject. "
        
        with open('secret/my_description.txt') as f:
            self.description = f.read().strip()
        
        self.message = ""
        
        with open('secret/google_api_credentials.json') as f:
            data = json.load(f)
            self.client = genai.Client(api_key=data["KEY"])
            self.model = "gemini-2.0-flash"

    def respond(self, message: str):
        response = self.client.models.generate_content(model=self.model, contents=message)
        return response.text
    
    def add_to_message(self, message: str):
        self.message += message
    
    def process_conversation(self):
        response = self.respond(self.system_prompt + " " + self.description + " " + self.message)
        self.message = ""
        return response