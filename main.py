from lib.web_interactor import WebInteractor
from lib.email_client import EmailClient
from lib.llm_agent import LLMAgent
from lib.file_saver import FileSaver
from lib.logger import logger

web_interactor = WebInteractor()
email_client = EmailClient()
llm_agent = LLMAgent()
file_saver = FileSaver()

web_interactor.load()
web_interactor.enter()
web_interactor.search()
urls = web_interactor.gather_results()

newly_responded = 0

for url in urls:
    advertisement_id, email_adress, html_content = web_interactor.visit_and_gather(url)
    
    has_been = file_saver.has_been_contacted(advertisement_id)
    
    if has_been:
        logger.info(f"Skipping {advertisement_id}")
        continue
    
    llm_agent.add_to_message(html_content)

    subject, response = llm_agent.process_conversation()

    email_client.gmail_send_message(
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

    file_saver.save_file(advertisement_id, information_json)
    
    newly_responded += 1

logger.info(f"Newly responded to: {newly_responded}")

web_interactor.close()
