import pytest
from src.personal_profile import PersonalProfile
from src.lib.llm_agent import LLMAgent
from src.lib.file_saver import FileSaver

@pytest.fixture
def profile():
    return PersonalProfile("michal")

def test_llm_agent_response(profile):
    llm_agent = LLMAgent(profile)
    response = llm_agent.respond("Tell me a quick joke.")
    assert len(response) != 0

def test_file_saver(profile):
    file_saver = FileSaver("flatfox.ch", profile)
    file_saver.save_file("test", {"key": "value"})
    file_saver.delete_file("test")
    
