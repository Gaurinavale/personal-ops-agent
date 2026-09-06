from langchain_mcp_adapters.client import MultiServerMCPClient

async def get_mcp_tools():
    """
    Connects to all 3 MCP servers — Task Manager, GitHub, and the
    ML Priority Predictor — and returns all their tools combined.
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
            "priority_predictor": {
                "command": "python",
                "args": ["-m", "ml_priority.server"],
                "transport": "stdio",
            },
        }
    )
    tools = await client.get_tools()
    return tools