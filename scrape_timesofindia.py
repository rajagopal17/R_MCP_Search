
import sys
import requests
from bs4 import BeautifulSoup
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
gemini_api_key = os.getenv("GEMINI_API_KEY")
# Load environment variables
load_dotenv()
client = genai.Client(api_key=gemini_api_key)
#create a agent with genai to scrape web page using mcp.json file:

#function to scrape times of india headline using mcp.json configuration:

tools_list = [{"tool_name": "search_web", "tool_description": "search internet for information"},
               {"tool_name": "get_current_time", "tool_description": "get the current time of any location"}]

user_query =input("Enter your query: ")


prompt=f''' you need to identify the right tool_name
         from given {tools_list} only  to answer {user_query}''',


tool_finder = client.models.generate_content(
                    model="gemini-2.5-flash",
                    
         
        contents= prompt)


                    
                



#print the identified tool
print("Identified tool to use:", tool_finder.text.strip())
