import httpx

def register_employee_tool(mcp):
    @mcp.tool()
    def get_employee_data() -> list:
        """Fetch employee data from the API"""
        try:
            response = httpx.get(
                "https://employees-data.azurewebsites.net/api/employee_data",
                timeout=1000  # Increase timeout to avoid early failures
            )
            response.raise_for_status()
            employee_data = response.json()  # Assuming the response is a list of employee data

            # Return employee data or process it as needed
            return employee_data

        except Exception as e:
            return f"❌ Error fetching employee data: {str(e)}"