import asyncio
import os

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment="gpt-4.1",
    azure_endpoint=os.getenv("AZURE_GPT41_API_BASE"),  # azure api base
    api_version=os.getenv("AZURE_GPT41_API_VERSION"),  # azure api version
    api_key=os.getenv("AZURE_GPT41_API_KEY"),  # azure api key
)


async def main():
    async with MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": [
                    "/home/toannguyen19/my_workspace/mcp/mcp-crash-course/servers/math_server.py"
                ],
            },
            "weather": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            },
        }
    ) as client:
        agent = create_react_agent(llm, client.get_tools())
        # result = await agent.ainvoke({"messages": "What is 2 + 2?"})
        result = await agent.ainvoke(
            {"messages": "What is the weather in San Francisco?"}
        )

        print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
