import asyncio
import mcp.server.stdio
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.types import Tool,TextContent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server = asyncio.Server("helloworld_server")
@server.list_tools()
async def list_tools():
    return [Tool( name ='hello_world', description=('Returns Hello, World!'),
            inputSchema={"type": "object", "properties": {}, "required": []}
               )
                 ]
           

@server.call_tool()
async def call_tool(tool_name:str, arguments):
    if tool_name == "hello_world":
        return TextContent(text="Hello, World!")
    else:
        return TextContent(text=f"Tool {tool_name} not found.")
    
async def main():
    server_params = mcp.server.stdio.StdioServerParameters(
        command="python",
        args=["helloworld_server.py"],
    )


