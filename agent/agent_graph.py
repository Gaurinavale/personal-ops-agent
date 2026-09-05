import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

from agent.mcp_client import get_mcp_tools

load_dotenv()  # loads GEMINI_API_KEY from .env into the environment


async def build_agent():
    """
    Builds a ReAct-style LangGraph agent wired to our MCP tools.
    """
    # 1. Set up the LLM that will do the reasoning
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
    )

    # 2. Fetch our MCP tools (add_task, list_tasks, complete_task)
    tools = await get_mcp_tools()

    # 3. Build the ReAct agent: LLM + tools, wired into a reasoning loop
    agent = create_react_agent(llm, tools)

    return agent