import httpx
from mcp.types import TextContent

# Google Custom Search API Key and Search Engine ID
google_api_key = "AIzaSyBiJrDXFspvd7HlNVlb2I_3051wKIN5XqE"
google_search_engine_id = "f42b20424611243cf"  # Your Custom Search Engine ID

# Google Custom Search API URL
google_search_api_url = "https://www.googleapis.com/customsearch/v1"

def register_tax_news_tool(mcp):
    @mcp.tool()
    def get_tax_changes(country_name: str) -> TextContent:
        """Fetch the latest tax changes using Google Custom Search API based on the country name"""
        try:
            # Construct the search query for tax-related news in the specified country
            query = f"Give me tax law changes from government of {country_name} as of 23rd july 2025"

            # Make a request to the Google Custom Search API
            response = httpx.get(
                google_search_api_url,
                params={
                    'q': query,  # The search query
                    'key': google_api_key,  # Google API key
                    'cx': google_search_engine_id,  # Custom Search Engine ID
                    'num': 5  # Number of results to fetch (maximum is 10)
                },
                timeout=10  # Timeout after 10 seconds
            )
            response.raise_for_status()  # Raise an exception for bad status codes

            # Parse the response JSON
            search_data = response.json()

            if 'items' in search_data:
                latest_news = []
                for item in search_data['items']:
                    title = item.get('title')
                    snippet = item.get('snippet')
                    link = item.get('link')
                    latest_news.append(f"Title: {title}\nSnippet: {snippet}\nLink: {link}\n")
                
                # Return the news content as a text response
                return TextContent(type="text", text="\n\n".join(latest_news))
            else:
                return TextContent(type="text", text="No recent tax changes found.")

        except httpx.TimeoutException:
            return TextContent(type="text", text="Timeout: API did not respond in time")

        except Exception as e:
            return TextContent(type="text", text=f"Error fetching tax news: {str(e)}")
