import httpx
from mcp.types import TextContent

def register_email_tool(mcp):
    @mcp.tool()
    def generate_email_id(employee_id: str) -> TextContent:
        """Generate official email ID using Employee ID"""
        try:
            print(f"Calling email generation API for Employee ID: {employee_id}...")

            response = httpx.post(
                "https://email-creation.azurewebsites.net/api/generate_email",
                json={"employee_ids": [employee_id]},
                timeout=10  # 10 seconds is sufficient
            )
            response.raise_for_status()

            emails = response.json().get("generated_emails", [])
            email = emails[0] if emails else "No email returned"
            print(f"Got email: {email}")

            return TextContent(type="text", text=email)

        except httpx.TimeoutException:
            return TextContent(type="text", text="Timeout: API did not respond in time")

        except Exception as e:
            return TextContent(type="text", text=f"Error generating email: {str(e)}")
