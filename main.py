from lib.web_interactor import WebInteractor
from lib.email_client import EmailClient
from lib.llm_agent import LLMAgent

interactor = WebInteractor()
email_client = EmailClient()
llm_agent = LLMAgent()

response = llm_agent.respond("Tell me a quick joke.")

print(response)

# for offer in interactor.select(5): # select top 5
    # context = interactor.scrape(offer)
    # message, adress = llm_agent.prepare(context)
    # email_client.contact(adress, message)
