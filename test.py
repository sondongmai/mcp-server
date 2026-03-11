import asyncio
from mcp.client.sse import sse_client
from mcp import ClientSession


async def test():
    async with sse_client("http://localhost:8999/mcp/sse") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List tools
            tools = await session.list_tools()
            print("✅ Tools:", [t.name for t in tools.tools])

            # Gọi sum_numbers
            result = await session.call_tool("sum_numbers", {"a": 10, "b": 20})
            print("✅ 10 + 20 =", result.content[0].text)


asyncio.run(test())