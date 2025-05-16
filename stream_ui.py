import streamlit as st
import httpx
import asyncio

# Function to fetch tools from the MCP server
async def fetch_tools(base_url):
    async with httpx.AsyncClient(timeout=60.0) as client:
        tools_response = await client.get(f"{base_url}/tools")
        if tools_response.status_code == 200:
            return tools_response.json().get("tools", [])
        else:
            st.error("Failed to fetch tools list")
            return []

# Function to call the selected tool and fetch its response
async def call_tool(base_url, tool_name, params):
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(f"{base_url}/mcp", json={
            "tool_name": tool_name,
            "params": params
        })
        
        if response.status_code == 200:
            if response.headers.get("content-type", "").startswith("application/json"):
                return response.json()
            else:
                st.error("Server did not return valid JSON.")
                return None
        else:
            st.error(f"Failed to call tool {tool_name}. Status code: {response.status_code}")
            return None

# Streamlit UI
def main():
    # Set up Streamlit UI
    st.title("MCP Server Tools Visualizer")
    
    base_url = "https://mcpserverapp.azurewebsites.net"
    
    # Fetch and display the list of tools
    st.sidebar.header("Select a Tool")
    tools = asyncio.run(fetch_tools(base_url))
    
    if tools:
        tool_name = st.sidebar.selectbox("Choose Tool", tools)
        
        if tool_name == "generate_email_id":
            st.subheader("Generate Email ID Tool")
            
            # Input fields for tool parameters
            first_name = st.text_input("First Name", "Alice")
            last_name = st.text_input("Last Name", "Johnson")
            
            # Call the tool and display the response
            if st.button("Generate Email"):
                params = {
                    "first_name": first_name,
                    "last_name": last_name
                }
                response = asyncio.run(call_tool(base_url, tool_name, params))
                
                if response:
                    st.write("Generated Email:", response)
        else:
            st.warning("No tool selected or invalid tool.")
    else:
        st.error("No tools found.")

if __name__ == "__main__":
    main()
