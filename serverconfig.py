from urllib import response
from fastmcp import FastMCP
import json
import os
from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent
from mcp import types
import sys

# Server instance configuration
mcp = FastMCP("QuickServer")
#####################################################
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
gemini_api_key = os.getenv("GEMINI_API_KEY")
# Load environment variables
load_dotenv()
client = genai.Client(api_key=gemini_api_key)
#####################################################
## Create tools :
import time

@mcp.tool()
def get_current_time() -> str:
    """
    Returns the current time in a human-readable format.
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

print("Tool 'get_current_time' registered.")

#function to search web using genai:
@mcp.tool()
def search_web(query: str) -> str:
    """
    Searches the web using GenAI and returns the results.
    """
    grounding_tool = types.Tool(
        google_search=types.GoogleSearch()
    )

    config = types.GenerateContentConfig(
        tools=[grounding_tool]
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=query,
        config=config,
    )

    return response.text

#
#run the server
if __name__ == "__main__":
        
    print("STARTING THE SERVER AT AMAZING LOCATION")

    
    
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run() # Run without transport for dev server
    else:
        # Start the server in a separate thread
        import threading
        server_thread = threading.Thread(target=lambda: mcp.run(transport="stdio"))
        server_thread.daemon = True
        server_thread.start()
        
        # Wait a moment for the server to start
        time.sleep(2)
        

        
        # Keep the main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")


