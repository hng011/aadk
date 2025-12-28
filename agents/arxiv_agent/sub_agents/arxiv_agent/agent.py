from . import settings
from google.adk.agents import LlmAgent
from agents.arxiv_agent.sub_agents.arxiv_agent.tools.search_paper_tool import search_paper 


DESCRIPTION = "An Agent that helps to explore arXiv site"

SYSTEM_INSTRUCTION = """
    You are a helpful assistant. 
    Your job is to fetch the latest papers from arXiv using the `search_latest_arxiv` tool. 
    The user will provide a domain of anything from general to a specific subject as a publication can be related to any kind of field
    The user might also specify a number of papers to fetch (e.g., 'get 5 papers') **MAXIMUM 7 PAPERS**. 
    If they don't specify a number, use the tool's default.
    When generating the response, make sure to include a concise explanation about the paper and the pdf, also source links
"""
    

arxiv_agent = LlmAgent(
    model=settings.MODEL_ID,
    name="arxiv_agent",
    description=DESCRIPTION,
    instruction=SYSTEM_INSTRUCTION,
    tools=[search_paper],
    output_key="paper_data"
)