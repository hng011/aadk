from . import settings

from google.adk.agents import Agent
from mcp_agent.mcp_config import (
    mcp_github_tool,
    mcp_huggingface_tool,
    mcp_context7_tool,
    # mcp_notion_tool,
)

SYSTEM_INSTRUCTION = """
Role: Act as a specialized Agent Navigator that connected to a lot of open-source tools. 
Your goal is to help users find the information needed based on the query

Output Requirements:
- Use Headings to separate different thing
- Use Tables for comparing multiple data.
- Use Bolding for key metrics like star counts or primary languages.
- Keep explanations concise and technical jargon accessible.

Your answer should be match to the language used by the user
"""

root_agent = Agent(
    model=settings.MODEL_ID,
    name="mcp_agent",
    instruction=SYSTEM_INSTRUCTION,
    tools=[
        mcp_github_tool(), 
        mcp_huggingface_tool(),
        mcp_context7_tool(),
        # mcp_notion_tool(),
    ],
)