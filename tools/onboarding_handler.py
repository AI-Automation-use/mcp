import httpx
from mcp.types import TextContent

def register_onboarding_tool(mcp):
    @mcp.tool()
    def trigger_onboarding_flow(
        caseId: str,
        fname: str,
        lname: str,
        personalEmail: str,
        officialEmail: str,
        attachmentPath: str
    ) -> TextContent:
        """Trigger onboarding and send email with attachment"""
        try:
            print(f"Triggering onboarding for {fname} {lname}...")

            response = httpx.post(
                "https://automated-notification-handler.azurewebsites.net/api/automated_notification_handler",
                json={
                    "caseId": caseId,
                    "fname": fname,
                    "lname": lname,
                    "personalEmail": personalEmail,
                    "officialEmail": officialEmail,
                    "attachmentPath": attachmentPath
                },
                timeout=10000
            )
            response.raise_for_status()

            result = response.text
            print(f"Raw response:{response}")
            print(result)
            print(f"Onboarding triggered successfully: {result}")

            return TextContent(type="text", text=result) 

        except httpx.TimeoutException:
            return TextContent(type="text", text="Timeout: Onboarding handler did not respond")

        except Exception as e:
            return TextContent(type="text", text=f"Error triggering onboarding: {str(e)}")
