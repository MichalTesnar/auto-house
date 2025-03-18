email_client_config = {
}

interactor_config = {
    "budget": [300, 600],
    "commute_endpoint": "ETH HG",
    "commute_limit_minutes": 30
}

llm_config = {
    "path_to_description": "string",
    "path_to_credentials": "string",
}

# interactor = WebInteractor(interactor_config)
# llm_agent = LLMAgent(llm_config)
# email_client = EmailClient(email_client_config)

# interactor.enter()

# interactor.filter()

# interactor.sort()

# interactor.select(5) 

# for offer in interactor.select(5): # select top 5
    # context = interactor.scrape(offer)
    # message, adress = llm_agent.prepare(context)
    # email_client.contact(adress, message)
