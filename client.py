import asyncio
import httpx
import json

MCP_URL = "http://localhost:8000/mcp"  # Or use Azure URL

async def call_mcp_tool(tool_name: str, params: dict, request_id: int = 1):
    payload = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": tool_name,
        "params": params
    }

    headers = {
    "Accept": "application/json, text/event-stream",
    "Content-Type": "application/json",
    "mcp-session-id": "employee-automation" 
}

    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.post(MCP_URL, json=payload, headers=headers)

        print("Status:", response.status_code)
        print("Headers:", response.headers)
        print("Raw Response:", response.text)

        if response.headers.get("content-type", "").startswith("application/json"):
            result = response.json()
            print("✅ MCP Result:")
            print(json.dumps(result, indent=2))
        else:
            print("❌ Invalid or non-JSON response")





# Example: generate_email_id
async def main():
    await call_mcp_tool("generate_email_id", {
        "first_name": "Alice",
        "last_name": "Johnson"
    })

    # Example: trigger_onboarding_flow
    await call_mcp_tool("trigger_onboarding_flow", {
        "caseId": 101,
        "fname": "Alice",
        "lname": "Johnson",
        "personalEmail": "alice.personal@example.com",
        "officialEmail": "alice.johnson01@sonata-software.com",
        "attachmentPath": "https://some.url/resume.pdf"
    })

if __name__ == "__main__":
    asyncio.run(main())
