from langchain_mcp_adapters.client import MultiServerMCPClient

async def get_mcp_tools():
    """
    Connects to BOTH MCP servers — Task Manager (Phase 1) and GitHub (Phase 4) —
    and returns all their tools combined, ready for the agent to use.
    """
    client = MultiServerMCPClient(
        {
            "task_manager": {
                "command": "python",
                "args": ["-m", "mcp_server.server"],
                "transport": "stdio",
            },
            "github": {
                "command": "python",
                "args": ["-m", "github_mcp.server"],
                "transport": "stdio",
            },
        }
    )
    tools = await client.get_tools()
    return tools