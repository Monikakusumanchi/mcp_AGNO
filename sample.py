import asyncio
import os
from dotenv import load_dotenv
import openai
from agno.agent import Agent
from agno.tools.mcp import MCPTools
from agno.utils.pprint import apprint_run_response
from agno.models.openai import OpenAIChat

# Load environment variables
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

async def run_agent(message: str) -> None:
    # Your OpenAI API key is now stored in the environment variable
    openai_api_key = os.getenv("OPENAI_API_KEY")

    async with MCPTools(
        command="npx mcp-remote http://127.0.0.1:7860/gradio_api/mcp/sse"
    ) as mcp_tools:
        # Create an OpenAI GPT agent
        agent = Agent(
            model=OpenAIChat("gpt-3.5-turbo",  # Use GPT-3.5 or GPT-4 based on your requirement
            api_key=openai_api_key),
            tools=[mcp_tools],
            markdown=True,
        )

        response_stream = await agent.arun(message, stream=True)
        await apprint_run_response(response_stream, markdown=True)

# if __name__ == "__main__":
#     asyncio.run(
#         run_agent(
#             "Count how many times the letter 'r' appears in the word 'strawberry'."
#         )
#     )

# if __name__ == "__main__":
#     asyncio.run(
#         run_agent(
#             "Use the tool to insert a user with ID 1, name 'Monika', task 'Data Entry', and description 'Testing MCP insert'."
#         )
#     )

if __name__ == "__main__":
    asyncio.run(
        run_agent(
            "show the users table data"
        )
    )
