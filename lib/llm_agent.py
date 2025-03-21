import json
from google import genai

class LLMAgent():
    def __init__(self):
        
        self.system_prompt = "You are a helpful assistant trying to help a student to get housing in the Zurich area by writing responses on an online website. You receive my description and information from the page in HTML format. Using relevant information, compile an email to the person offering the house introducing me and expressing interest in the offer in an approapriate language (language they use for communication, as listed). If German is listed, try to stick to Schweizerhochdeutsch. Use any keywords they say you should mention, or to the best of your knowledge answer any questions or relevant information they ask for. Answer with <subject>enter subject here</subject> and <response>enter response here</response>. Do not provide any other description or explanation around this message, just the message itself."
        
        with open('secret/my_description.json') as f:
            data = json.load(f)
            self.description = str(data)
        
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
        llm_response = self.respond(self.system_prompt + " " + self.description + " " + self.message)
        self.message = ""
        
        subject_start = llm_response.find("<subject>") + len("<subject>")
        subject_end = llm_response.find("</subject>")
        response_start = llm_response.find("<response>") + len("<response>")
        response_end = llm_response.find("</response>")
        
        subject = llm_response[subject_start:subject_end].strip()
        response = llm_response[response_start:response_end].strip()
        
        return subject, response