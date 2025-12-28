from . import settings
from google.adk.agents import LlmAgent
from agents.arxiv_agent.sub_agents.reviewer_agent.tools.review_paper_tool import review_paper_tool


DESCRIPTION = "An Agent that helps to get the paper's' urls"

SYSTEM_INSTRUCTION = """
    You are a helpful assistant. 
    
    here is the summary from previous agent

    {paper_data}

    Always use `review_paper_tool` tool where the input is the string of source with `abs` keyword and pdf urls with `pdf` keyword in the url
"""
    
reviewer_agent = LlmAgent(
    model=settings.MODEL_ID,
    name="reviewer_agent",
    description=DESCRIPTION,
    instruction=SYSTEM_INSTRUCTION,
    output_key="reviewed_paper",
    tools=[
        review_paper_tool
    ]
)