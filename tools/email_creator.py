import httpx
from mcp.types import TextContent

def register_email_tool(mcp):
    @mcp.tool()
    def generate_email_id(first_name: str, last_name: str) -> TextContent:
        """Generate official email ID from first and last name"""
        try:
            print(f"Calling email generation API for {first_name} {last_name}...")

            response = httpx.post(
                "https://email-creation.azurewebsites.net/api/generate_email",
                json={"first_name": first_name, "last_name": last_name},
                timeout=10000
            )
            response.raise_for_status()

            email = response.json().get("email_id", "No email returned")
            print(f"Got email: {email}")

            return TextContent(type="text", text=email)  

        except httpx.TimeoutException:
            return TextContent(type="text", text="Timeout: API did not respond in time")

        except Exception as e:
            return TextContent(type="text", text=f"Error generating email: {str(e)}")
