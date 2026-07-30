import asyncio
import json
import os
from mcp import ClientSession
from mcp.client.sse import sse_client
from openai import AsyncOpenAI

# Initialize OpenAI client
client = AsyncOpenAI(
    base_url= "https://eus2.openai.azure.com/openai/v1",
    api_key="pBJqqwwAKD6yHwewYoowo"
    )
MODEL = "EGPT-4.1" # axure open ai (foundary) deployment name

SYSTEM_PROMPT = """\
You are an AI assistant for Tool Calling.

Before you help a user, you need to work with tools to interact with Our Database.
"""

def mcp_tools_to_openai_format(tools) -> list[dict]:
    """Convert MCP tool definitions to OpenAI function-calling format."""
    openai_tools = []
    for tool in tools:
        openai_tools.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description or "",
                "parameters": tool.inputSchema if tool.inputSchema else {"type": "object", "properties": {}},
            },
        })
    return openai_tools


async def run_agent_loop(session: ClientSession, user_message: str, verbose: bool = False) -> str:
    """Run an agentic loop using OpenAI with MCP tools."""
    tools_result = await session.list_tools()
    openai_tools = mcp_tools_to_openai_format(tools_result.tools)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    while True:
        response = await client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=openai_tools if openai_tools else None,
            tool_choice="auto" if openai_tools else None,
        )

        message = response.choices[0].message
        messages.append(message.model_dump(exclude_unset=False))

        # No tool calls — return the final answer
        if not message.tool_calls:
            return message.content or ""

        # Process each tool call
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            if verbose:
                print(f"  [tool call] {tool_name}({tool_args})")

            result = await session.call_tool(tool_name, tool_args)
            tool_output = result.content[0].text if result.content else ""

            if verbose:
                print(f"  [tool result] {tool_name} -> {tool_output}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_output,
            })


async def main():
    server_url = "http://127.0.0.1:8000/sse"

    async with sse_client(server_url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Show available tools
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"  {tool.name}: {tool.description}")

            print("\nEnter 'exit' to quit")
            while True:
                try:
                    user_input = input("\nEnter your message: ")
                    if user_input.lower() == "exit":
                        break

                    print(f"\nUser: {user_input}")
                    response = await run_agent_loop(session, user_input, verbose=True)
                    print(f"Agent: {response}")

                except KeyboardInterrupt:
                    print("\nExiting...")
                    break
                except Exception as e:
                    print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
