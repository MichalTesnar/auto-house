import json
from google import genai

class LLMAgent():
    def __init__(self):
        
        self.system_prompt = "You are an online bot writing responses for me to offers about housing. You will receive my description, and you will receive description about the house in HTML format. Using relevant information, compile an email to the person offering the house introducing me and expressing interest in the offer in an approapriate language. Use any keywords they say you should mention. Do not provide any other description or explanation around this message, just the message itself. Do not include subject. "
        
        self.description = "Hey,Your shared apartment life sounds exactly like what I’m looking for – calm, relaxed, and with friendly roommates. I’m pretty easygoing and appreciate a harmonious atmosphere. Since I’m studying and working on the side, I’m usually busy, but I enjoy having good conversations or just spending a relaxed time in between. I also really like the room! I’d definitely be interested in taking over the furniture, so that wouldn’t be a problem for me. If you’d like to learn a bit more about me in advance, feel free to check out my LinkedIn profile (https://www.linkedin.com/in/michal-tesnar/) or my blog (https://michaltesnar.github.io/). If it works for you, I’d love to meet you in person and take a look at the room. Just let me know when it suits you best! My name is Michal Tešnar. My phone number is +41 78 441 32 32, my email is michal.tesnar007@gmail.com."
        
        self.message = ""
        
        with open('secret/aistudio_credentials.json') as f:
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