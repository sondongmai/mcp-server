import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client


async def main():
    async with sse_client("http://localhost:8999/mcp/") as streams:
        async with ClientSession(*streams) as session:

            await session.initialize()

            tools = await session.list_tools()
            print("TOOLS:", len(tools))

            result = await session.call_tool(
                "roll_dice",
                {"sides": 6}
            )

            print("RESULT:", result)


asyncio.run(main())