import asyncio
from mcp.server.fastmcp import FastMCP
from mcp.server.streamable_http import StreamableHTTPServerTransport
from tools.email_creator import register_email_tool
from tools.onboarding_handler import register_onboarding_tool

# Initialize MCP and transport globally
mcp = FastMCP("Employee Automation Server")
register_email_tool(mcp)
register_onboarding_tool(mcp)

transport = StreamableHTTPServerTransport(
    mcp_session_id="employee-automation"
)

# Expose ASGI app via MCP's streamable HTTP method
app = mcp.streamable_http_app()

# Setup MCP execution logic on startup
@app.on_event("startup")
async def startup():
    await transport.connect()
    asyncio.create_task(mcp.run_streamable_http_async())
