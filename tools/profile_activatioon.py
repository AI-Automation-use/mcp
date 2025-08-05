import httpx
from mcp.types import TextContent

def register_profile_activation_tool(mcp):
    @mcp.tool()
    def activate_profile(employee_id: str) -> TextContent:
        """Activate employee profile using Employee ID"""
        try:
            print(f"Calling Profile Activation API for Employee ID: {employee_id}...")

            response = httpx.post(
                "https://darwin-active.azurewebsites.net/api/activate_employee?",
                json={"employee_ids": [employee_id]},
                timeout=10  # shorter and reasonable timeout
            )
            response.raise_for_status()

            activation_data = response.json().get("activation_results", {})
            message = activation_data.get(employee_id, "No activation result found")

            print(f"Got message: {message}")
            return TextContent(type="text", text=message)

        except httpx.TimeoutException:
            return TextContent(type="text", text="Timeout: API did not respond in time")

        except Exception as e:
            return TextContent(type="text", text=f"Error Activating Profile: {str(e)}")
