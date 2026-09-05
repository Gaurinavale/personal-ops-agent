import asyncio
from agent.agent_graph import build_agent


async def chat():
    print("🤖 Personal Ops Agent — type 'exit' to quit\n")

    agent = await build_agent()

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            print("Goodbye!")
            break

        # Send the user's message to the agent
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": user_input}]}
        )

        # The agent's final reply is the last message in the returned state
        final_message = result["messages"][-1]
        content = final_message.content

        if isinstance(content, list):
            # Extract just the text parts from structured content blocks
            text = "".join(
                block.get("text", "") for block in content if isinstance(block, dict)
            )
        else:
            text = content

        print(f"Agent: {text}\n")


if __name__ == "__main__":
    asyncio.run(chat())