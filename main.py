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
html_content = web_interactor.visit_and_gather(urls[0])

llm_agent.add_to_message(html_content)

response = llm_agent.process_conversation()

email_client.gmail_send_message(
    "tesnarmm@gmail.com",
    "Interest in Room Posted on Online",
    response
)

web_interactor.close()
