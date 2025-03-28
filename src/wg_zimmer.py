from src.lib.wg_zimmer_web_interactor import WGZimmerWebInteractor
from src.lib.email_client import EmailClient
from src.lib.llm_agent import LLMAgent
from src.lib.file_saver import FileSaver
from src.lib.logger import logger

class WGZimmer():
    def __init__(self, profile, debug_mode=False):
        self.web_interactor = WGZimmerWebInteractor(profile)
        self.email_client = EmailClient(profile)
        self.llm_agent = LLMAgent(profile)
        self.file_saver = FileSaver("wgzimmer.ch", profile)
        self.debug_mode = debug_mode
        
        self.urls = []
        
    def search(self):
        self.web_interactor.load()
        self.web_interactor.enter()
        self.web_interactor.search()
        self.urls = self.web_interactor.gather_results()
        
    def run(self):
        newly_responded = 0
        
        while self.web_interactor.has_next_link:
            advertisement_id, html_content = self.web_interactor.visit_and_gather()
            
            has_been = self.file_saver.has_been_contacted(advertisement_id)
            
            if has_been:
                logger.info(f"Skipping {advertisement_id}")
                continue
            
            self.llm_agent.add_to_message(html_content)

            subject, response = self.llm_agent.game_conversation()
            
            if self.debug_mode:
                print(subject, response)
                exit()

            information_json = {
                "id": advertisement_id,
                "subject": subject,
                "response": response
                }
            
            self.web_interactor.send_information(response)

            self.file_saver.save_file(advertisement_id, information_json)
            
            newly_responded += 1

        logger.info(f"Newly responded to: {newly_responded}")

        self.web_interactor.close()
