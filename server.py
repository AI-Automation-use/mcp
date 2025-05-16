import asyncio
from mcp.server.fastmcp import FastMCP
from mcp.server.streamable_http import StreamableHTTPServerTransport
from tools.email_creator import register_email_tool
from tools.onboarding_handler import register_onboarding_tool

async def main():
    mcp = FastMCP("Employee Automation Server")

    # Register tools
    register_email_tool(mcp)
    register_onboarding_tool(mcp)

    # Setup transport
    transport = StreamableHTTPServerTransport(mcp_session_id="employee-automation")

    async with transport.connect():
        await mcp.run_streamable_http_async()

if __name__ == "__main__":
    asyncio.run(main())
