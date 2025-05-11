import asyncio
import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import getpass
load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment="gpt-4.1",
    azure_endpoint = os.getenv("AZURE_GPT41_API_BASE"),                 # azure api base
    api_version = os.getenv("AZURE_GPT41_API_VERSION"),           # azure api version
    api_key = os.getenv("AZURE_GPT41_API_KEY"),                   # azure api key
)    


stdio_server_params = StdioServerParameters(
    command="python",
    args=["/home/toannguyen19/my_workspace/mcp/mcp-crash-course/servers/math_server.py"],
)

async def main():
    async with stdio_client(stdio_server_params) as (read,write):    
        async with ClientSession(read_stream=read, write_stream=write) as session:
            await session.initialize()
            print("session initialized")
            tools = await load_mcp_tools(session)


            agent = create_react_agent(llm,tools)

            result = await agent.ainvoke({"messages": [HumanMessage(content="What is 54 + 2 * 3?")]})
            print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())

