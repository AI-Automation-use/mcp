import asyncio
from mcp.server.fastmcp import FastMCP
from mcp.server.streamable_http import StreamableHTTPServerTransport
from tools.email_creator import register_email_tool
from tools.onboarding_handler import register_onboarding_tool
from tools.profile_activatioon import register_profile_activation_tool
from tools.employee_details import register_employee_tool
from tools.update_emp_details import register_email_update_tool
from tools.tax_changes import register_tax_news_tool
from tools.email_drafter import register_draft_email_tool
# from mcp.server.auth. import 
# Initialize MCP and transport
mcp = FastMCP("Employee Automation Server")
register_email_tool(mcp)
register_onboarding_tool(mcp)
register_profile_activation_tool(mcp)
register_employee_tool(mcp)
register_email_update_tool(mcp)
register_tax_news_tool(mcp)
register_draft_email_tool(mcp)
transport = StreamableHTTPServerTransport(
    mcp_session_id="employee-automation"
)

#ASGI app via MCP's streamable HTTP method
app = mcp.streamable_http_app()

#execution logic on startup
@app.on_event("startup")
async def startup():
    await transport.connect()
    asyncio.create_task(mcp.run_streamable_http_async())

