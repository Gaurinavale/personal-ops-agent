import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

from agent.mcp_client import get_mcp_tools
from agent.memory import save_memory, recall_memory

load_dotenv()


async def build_agent():
    """
    Builds a ReAct-style LangGraph agent wired to our MCP tools.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
    )

    tools = await get_mcp_tools()
    agent = create_react_agent(llm, tools)

    return agent


async def chat_with_memory(agent, user_input: str) -> str:
    """
    Wraps a single chat turn with memory: recalls relevant past context,
    injects it into the conversation, runs the agent, then saves a summary.
    """
    # 1. Recall relevant memories based on the current message
    memories = recall_memory(user_input, k=3)
    memory_context = "\n".join(memories) if memories else "No relevant past memory."

    # 2. Build the message list, including memory as system context
    messages = [
        {
            "role": "system",
            "content": f"Relevant memory from past conversations:\n{memory_context}",
        },
        {"role": "user", "content": user_input},
    ]

    # 3. Run the agent as before
    result = await agent.ainvoke({"messages": messages})
    final_message = result["messages"][-1]
    content = final_message.content

    if isinstance(content, list):
        text = "".join(block.get("text", "") for block in content if isinstance(block, dict))
    else:
        text = content

    # 4. Save this exchange to long-term memory
    save_memory(f"User asked: {user_input}\nAgent replied: {text}")

    return text