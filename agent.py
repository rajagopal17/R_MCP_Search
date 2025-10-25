import asyncio
import time
import os
import datetime
import logging
import ast
import mcp.server.stdio


from mcp import ClientSession, StdioServerParameters, Tool
from mcp.client.stdio import stdio_client

logging.basicConfig(level=logging.INFO)

def get_current_time() -> str:
    """Get the current date and time in a specific format."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

server = asyncio.Server("helloworld_server")
async def main(user_input: str):
    print("[agent] Starting agent...")
    print(f"[agent] Current working directory: {os.getcwd()}")
    
    server_params = StdioServerParameters(
        command="python",
        args=["helloworld_server.py"],
    )


    

