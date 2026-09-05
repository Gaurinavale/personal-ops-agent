from langchain_mcp_adapters.client import MultiServerMCPClient

async def get_mcp_tools():
    """
    Connects to our local MCP Task Manager server (Phase 1) and
    returns its tools in a format LangGraph agents can call directly.
    """
    client = MultiServerMCPClient(
        {
            "task_manager": {
                "command": "python",
                "args": ["-m", "mcp_server.server"],
                "transport": "stdio",
            }
        }
    )
    tools = await client.get_tools()
    return tools