import json
from google import genai
import re


class LLMAgent():
    def __init__(self, profile):
        self.profile = profile
        
        self.system_prompt = "You are a helpful assistant trying to help a student to get housing in the Zurich area by writing responses on an online website. You receive my description and information from the page in HTML format, as well as tips on writing an effective message. Using relevant information, compile an email to the person offering the house introducing me and expressing interest in the offer in an approapriate language (language they use for communication, as listed). If German is listed, try to stick to Schweizerhochdeutsch. Avoid overly complex and fancy phrases, use relaxed tone and simple vocabulary, more typical for a student. Use any keywords they say you should mention, or to the best of your knowledge answer any questions or relevant information they ask for. You do not need to forcefully include all the information I provide you with in my description, just what you feel is relevant. Answer with <subject>enter subject here</subject> and <response>enter response here</response>. Do not provide any other description or explanation around this message, just the message itself."
        
        self.gaming_prompt = "You are a helpful assistant trying to help a student to get housing in the Zurich area by writing responses on an online website. You are provided information from the website in HTML format, try to identify the person or group behind the message who will likely receive your message, and how should the message look to catch their eye. Notice cues mentioned in the message. Come up with unique subject line for an email for the student. Summarize the conclusions in a small guide for the student to write a message."
        
        
        self.message = ""
        self.client = genai.Client(api_key=self.profile.api_key)
        self.model = "gemini-2.0-flash"

    def respond(self, message: str):
        response = self.client.models.generate_content(model=self.model, contents=message)
        response_clean = re.sub(r'[^\u0000-\uFFFF]', '', response.text)
        
        return response_clean
    
    def add_to_message(self, message: str):
        self.message += message
    
    def process_conversation(self):
        llm_response = self.respond(self.system_prompt + " " + self.profile.description + " " + self.message)
        self.message = ""
        
        subject_start = llm_response.find("<subject>") + len("<subject>")
        subject_end = llm_response.find("</subject>")
        response_start = llm_response.find("<response>") + len("<response>")
        response_end = llm_response.find("</response>")
        
        subject = llm_response[subject_start:subject_end].strip()
        response = llm_response[response_start:response_end].strip()
        
        return subject, response
    
    def game_conversation(self):
        game_instructions = self.respond(self.gaming_prompt + self.message)
        llm_response = self.respond(self.system_prompt + " " + self.profile.description + " " + game_instructions + " " + self.message)
        self.message = ""
        
        subject_start = llm_response.find("<subject>") + len("<subject>")
        subject_end = llm_response.find("</subject>")
        response_start = llm_response.find("<response>") + len("<response>")
        response_end = llm_response.find("</response>")
        
        subject = llm_response[subject_start:subject_end].strip()
        response = llm_response[response_start:response_end].strip()
        
        return subject, response
        