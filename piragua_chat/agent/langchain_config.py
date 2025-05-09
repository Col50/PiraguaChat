import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from piragua_chat.agent.tools.get_document_tool import get_document_tool
from piragua_chat.agent.tools.get_physicochemical_report_tool import (
    get_physicochemical_report_tool,
)
from piragua_chat.agent.tools.get_hydrobiological_report_tool import (
    get_hydrobiological_report_tool,
)
from piragua_chat.agent.tools.get_todays_date_tool import get_todays_date_tool

load_dotenv()

# === Tools ===
tools = [
    get_document_tool,
    get_physicochemical_report_tool,
    get_hydrobiological_report_tool,
    get_todays_date_tool,
]

tool_list = {tool.name: tool for tool in tools}

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro-latest",
    api_key=os.getenv("GENAI_API_KEY"),
    temperature=0.3,
)

llm_with_tools = llm.bind_tools(tools)
