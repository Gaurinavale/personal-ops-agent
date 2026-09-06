import asyncio
from agent.agent_graph import build_agent, chat_with_memory


async def chat():
    print("🤖 Personal Ops Agent — type 'exit' to quit\n")

    agent = await build_agent()

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            print("Goodbye!")
            break

        text = await chat_with_memory(agent, user_input)
        print(f"Agent: {text}\n")


if __name__ == "__main__":
    asyncio.run(chat())