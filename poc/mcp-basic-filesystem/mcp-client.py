# /// script
# requires-python = "==3.12"
# dependencies = ["fastmcp>=2.10.0", "google-genai>=1.29.0"]
# ///

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from google import genai

GEMINI_API_KEY = "YOUR_API_KEY"
ALLOW_DIRECTORY = (
    "YOUR_PATH_FOR_LLM_TO_USE"  # NOTE: Need to create it MANUALLY in advance.
)

client = genai.Client(api_key=GEMINI_API_KEY)

# It spins up the MCP server when needed, i.e. it is not long running.
server_params = StdioServerParameters(
    command="npx",
    args=[
        "-y",
        "@modelcontextprotocol/server-filesystem",
        ALLOW_DIRECTORY,
    ],
)


async def create_hello_world_with_filesystem_mcp():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Prompt to let gemini model conduct a task with leveraging the local MCP defined above.
            # You should expect gemini will create the "abc" folder under the ALLOW_DIRECTORY. And
            # also create a "hello_world.py" script with logic implemented.
            prompt = f"create a hello_world.py with logic implemented under '{ALLOW_DIRECTORY}/abc'."

            # Initialize the connection between client and server
            await session.initialize()

            # Send request to the model with MCP function declarations
            response = await client.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    temperature=0,
                    tools=[
                        session
                    ],  # (Nice to know) uses the session, will automatically call the tool
                    # Uncomment if you **don't** want the SDK to automatically call the tool
                    # automatic_function_calling=genai.types.AutomaticFunctionCallingConfig(
                    #     disable=True
                    # ),
                ),
            )
            print(response.text)


# Execute the demo.
asyncio.run(create_hello_world_with_filesystem_mcp())
