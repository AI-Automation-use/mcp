import httpx
from mcp.types import TextContent

def register_email_update_tool(mcp):
    @mcp.tool()
    def update_employee_email(employee_id: str, generated_email: str) -> TextContent:
        """Update the employee's email ID in the provisioning system."""
        try:
            print(f"Calling Email Update API for Employee ID: {employee_id} with Email: {generated_email}...")

            response = httpx.post(
                "https://update-email.azurewebsites.net/api/update_employee_email",
                json={
                    "employee_id": employee_id,
                    "generated_email": generated_email
                },
                timeout=10  # reasonable timeout in seconds
            )
            response.raise_for_status()

            update_status = response.json().get("message", "No message returned")
            print(f"Email update status: {update_status}")

            return TextContent(type="text", text=update_status)

        except httpx.TimeoutException:
            return TextContent(type="text", text="Timeout: API did not respond in time")

        except Exception as e:
            return TextContent(type="text", text=f"Error updating email: {str(e)}")
