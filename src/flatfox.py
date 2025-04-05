from src.lib.flatfox_web_interactor import FlatfoxWebInteractor
from src.lib.email_client import EmailClient
from src.lib.llm_agent import LLMAgent
from src.lib.file_saver import FileSaver
from src.lib.logger import logger

DEBUG = 0

class Flatfox():
    def __init__(self, profile):
        self.email_client = EmailClient(profile)
        self.web_interactor = FlatfoxWebInteractor(profile, self.email_client) # @TODO: I do not like this construction!
        self.llm_agent = LLMAgent(profile)
        self.file_saver = FileSaver("flatfox.ch", profile)
        
        self.urls = []
        
    def search(self):
        self.web_interactor.load()
        self.web_interactor.enter()
        self.web_interactor.search()
        self.urls = self.web_interactor.gather_results()
        
    def run(self):
        
        newly_responded = 0
        
        for url in self.urls:
            advertisement_id, email_adress, html_content = self.web_interactor.visit_and_gather(url)
            
            has_been = self.file_saver.has_been_contacted(advertisement_id)
            
            if has_been:
                logger.info(f"Skipping {advertisement_id}")
                continue
            
            self.llm_agent.add_to_message(html_content)

            subject, response = self.llm_agent.game_conversation()
            
            if DEBUG:
                print(subject, response)
                exit()

            self.email_client.gmail_send_message(
                email_adress,
                subject,
                response
            )
            
            information_json = {
                "id": advertisement_id,
                "email_adress": email_adress,
                "subject": subject,
                "response": response
                }

            self.file_saver.save_file(advertisement_id, information_json)
            
            newly_responded += 1

        logger.info(f"Newly responded to: {newly_responded}")

        self.web_interactor.close()
