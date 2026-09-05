from mcp_server.db import init_db
from mcp_server.tools import mcp

if __name__ == "__main__":
    # Ensure the database and table exist before the server starts
    init_db()
    # Start the MCP server — this blocks and listens for a client
    mcp.run()