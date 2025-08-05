from mcp.types import TextContent
from openai import AzureOpenAI

# Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint="https://summarize-gen.openai.azure.com/",
    api_key="1DkyvFGwRKbcWKFYxfGAot2s8Qc9UPM8NmsbJR2OJDWJTBs084usJQQJ99ALACHYHv6XJ3w3AAABACOGvGzF",
    api_version="2025-01-01-preview"
)

def register_draft_email_tool(mcp):
    @mcp.tool()
    def draft_email(user_prompt: str) -> TextContent:
        """
        Draft an email based on a natural language instruction (e.g., 'Send a thank you email to John for the support').
        The tool will infer the recipient, subject, tone, and content using the AI model.
        """

        prompt = (
            "You are a professional email assistant.\n"
            "The user will provide a request in natural language.\n"
            "Your task is to generate a complete email based on the user's intent.\n"
            "You must:\n"
            "- Identify the recipient's name (if mentioned)\n"
            "- Infer the subject and tone\n"
            "- Draft a professional HTML-formatted email body\n"
            "Output only the complete email body in HTML. Do not include metadata.\n\n"
            f"User request: {user_prompt}"
        )

        try:
            response = client.chat.completions.create(
                model="o3-mini",
                max_completion_tokens=100000,
            reasoning_effort="low",
            
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that writes formal and contextual HTML emails."},
                    {"role": "user", "content": prompt}
                ]
            )

            html_body = response.choices[0].message.content
            return TextContent(type="text", text=html_body)

        except Exception as e:
            return TextContent(type="text", text=f"Error generating email: {str(e)}")
