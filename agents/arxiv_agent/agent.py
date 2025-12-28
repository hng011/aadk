from . import settings
from google.adk.agents import SequentialAgent
from agents.arxiv_agent.sub_agents.arxiv_agent.agent import arxiv_agent
from agents.arxiv_agent.sub_agents.reviewer_agent.agent import reviewer_agent


root_agent = SequentialAgent(
    name="research_agent",
    description="""
    Executes all the agents sequentially
    """,
    sub_agents=[
        arxiv_agent,
        reviewer_agent
    ]
)