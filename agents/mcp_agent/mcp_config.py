from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import (
    StreamableHTTPServerParams,
)

from . import settings

def mcp_github_tool() -> McpToolset:
    return McpToolset(
        connection_params=StreamableHTTPServerParams(
        url="https://api.githubcopilot.com/mcp/",
        headers={
            "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
            "X-MCP-Toolsets": "all",
            "X-MCP-Readonly": "true"
        },
    ),
)
    
    
def mcp_huggingface_tool() -> McpToolset:
    return McpToolset(
        connection_params=StreamableHTTPServerParams(
            url="https://huggingface.co/mcp",
            headers={
                "Authorization": f"Bearer {settings.HUGGING_FACE_TOKEN}"
            }
        )
    )


def mcp_notion_tool() -> McpToolset:
    pass


# External MCP tool

def mcp_context7_tool() -> McpToolset:
    return McpToolset(
        connection_params=StreamableHTTPServerParams(
            url="https://mcp.context7.com/mcp",
            headers={
                "CONTEXT7_API_KEY": f"{settings.CONTEXT7_TOKEN}"
            }
        )
    )
