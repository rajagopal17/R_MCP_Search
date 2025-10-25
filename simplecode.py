from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from google import genai
from dotenv import load_dotenv
import os
import asyncio
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
#########################################################


api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

#########################################################

async def main():

    
    # Create a single MCP Multiply server connection
    print("Establishing connection to RAG server...")
    server_params = StdioServerParameters(
        command="python",
        args=["serverconfig.py"]
    )
    
       
    async with stdio_client(server_params) as (read, write):
        
        print("Connection established, creating session...")
        async with ClientSession(read, write) as session:
            
    
             print("Session created, initializing...")
             await session.initialize()
             

             # Get available tools
             print("Requesting tool list...")
             tools = await session.list_tools()
             
        
             print("Tools available:")
            #print(tools.model_dump())
  
                    
             tools_description = []
             tools_list = []
             for i in range(0,len(tools.tools)):
                tools_list.append(tools.tools[i].name)

        
             print(f"Tools list: {tools_list}")    
             for i in range(0,len(tools.tools)):
                print(f"Tool_{i+1}: {tools.tools[i].name} - {tools.tools[i].description}")
                tools_description.append(f"{tools.tools[i].name}: {tools.tools[i].inputSchema.values()}")

                
             # print(f"Tools description:{tools_description}")
           #################################################################
             user_query = input("Enter your query: ")

             prompt=f''' you need to identify the right tool_name from the 
         from given {tools_list} only  to answer {user_query}''',


             tool_finder = client.models.generate_content(
                    model="gemini-2.5-flash",
                    
         
             contents= prompt)

             identified_tool = tool_finder.text.strip()
             print(f"Identified tool to use: {identified_tool}")

            ###############################################################
             # Prepare arguments for the selected tool
             tool_args = {}
             if identified_tool == "search_web":
                 tool_args = {"query": user_query}

                 print({"\n\ntool_args identified": tool_args})
             elif identified_tool == "get_current_time":
                 # This tool takes no arguments
                 tool_args = {"query": user_query}
                 print({"\n\ntool_args identified": tool_args})

             final_response = await session.call_tool(name=identified_tool, arguments=tool_args)
             # Process the final response:
             print(f"\nFinal Response from MCP server:\n{final_response}")
             #run the tool and get the response:


# Run the main async function
if __name__ == "__main__":
    asyncio.run(main())
