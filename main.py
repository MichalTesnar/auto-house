from lib.web_interactor import WebInteractor
from lib.email_client import EmailClient
from lib.llm_agent import LLMAgent

web_interactor = WebInteractor()
email_client = EmailClient()
llm_agent = LLMAgent()

web_interactor.load()
web_interactor.enter()
web_interactor.search()
urls = web_interactor.gather_results()
web_interactor.visit_and_gather(urls[0])
web_interactor.close()
