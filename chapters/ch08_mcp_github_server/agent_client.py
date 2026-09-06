# agent_client.py
import anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

client = anthropic.Anthropic()


async def run_task(task):
    server_params = StdioServerParameters(command="python", args=["server.py"])

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools_response = await session.list_tools()
            tools = [
                {"name": t.name, "description": t.description, "input_schema": t.inputSchema}
                for t in tools_response.tools
            ]

            messages = [{"role": "user", "content": task}]
            response = client.messages.create(
                model="your-provider-model-name",
                max_tokens=1000,
                tools=tools,
                messages=messages
            )

            # Handle tool calls in a loop until the model produces a final answer.
            # This IS the perceive-decide-act-observe cycle from Chapter 1, made
            # completely explicit in code for the first time in this book.
            while response.stop_reason == "tool_use":
                tool_use = next(b for b in response.content if b.type == "tool_use")
                result = await session.call_tool(tool_use.name, tool_use.input)
                messages.append({"role": "assistant", "content": response.content})
                messages.append({
                    "role": "user",
                    "content": [{"type": "tool_result", "tool_use_id": tool_use.id, "content": str(result.content)}]
                })
                response = client.messages.create(
                    model="your-provider-model-name",
                    max_tokens=1000,
                    tools=tools,
                    messages=messages
                )
            return response.content[0].text
