from src.lib.flatfox_web_interactor import FlatfoxWebInteractor
from src.lib.email_client import EmailClient
from src.lib.llm_agent import LLMAgent
from src.lib.file_saver import FileSaver
from src.lib.logger import logger

import time

DEBUG = 0

class Flatfox():
    def __init__(self, profile, confirmation_mode=False):
        self.email_client = EmailClient(profile)
        self.web_interactor = FlatfoxWebInteractor(profile, self.email_client) # @TODO: I do not like this construction!
        self.llm_agent = LLMAgent(profile)
        self.file_saver = FileSaver("flatfox.ch", profile)

        self.confirmation_mode = confirmation_mode
        
        self.urls = []
        
    def search(self):
        self.web_interactor.load()
        self.web_interactor.enter()
        self.web_interactor.search()
        self.urls = self.web_interactor.gather_results()
        
    def run(self):
        
        newly_responded = 0
        
        for url in self.urls:
            advertisement_id, html_content = self.web_interactor.visit_and_gather(url)
            
            has_been = self.file_saver.has_been_contacted(advertisement_id)
            
            if has_been:
                logger.info(f"Skipping {advertisement_id}")
                continue
            
            self.llm_agent.add_to_message(html_content)

            subject, response = self.llm_agent.game_conversation()
            
            information_json = {
                "id": advertisement_id,
                "subject": subject,
                "response": response
                }
            
            if self.confirmation_mode:
                self.file_saver.save_file("temporary", information_json)
                input(f"Go and edit temporary file, then come back and press enter!")
                information_json = self.file_saver.load_edited_file_and_delete("temporary")
                print("Ok, sending the message!")
                response = information_json["response"]
                subject = information_json["subject"]
            
            self.web_interactor.send_information(response)

            self.file_saver.save_file(advertisement_id, information_json)
            
            time.sleep(1)
            
            newly_responded += 1
            
        logger.info(f"Newly responded to: {newly_responded}")

        self.web_interactor.close()
