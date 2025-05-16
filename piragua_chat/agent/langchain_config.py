import os
from dotenv import load_dotenv

from piragua_chat.agent.tools.get_document_tool import get_document_tool
from piragua_chat.agent.tools.get_physicochemical_report_tool import (
    get_physicochemical_report_tool,
)
from piragua_chat.agent.tools.get_hydrobiological_report_tool import (
    get_hydrobiological_report_tool,
)
from piragua_chat.agent.tools.get_todays_date_tool import get_todays_date_tool

from langchain_openai import ChatOpenAI

load_dotenv()

# === Tools ===
tools = [
    get_document_tool,
    get_physicochemical_report_tool,
    get_hydrobiological_report_tool,
    get_todays_date_tool,
]

tool_list = {tool.name: tool for tool in tools}

llm = ChatOpenAI(
    model="gpt-4",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.3,
)

llm_with_tools = llm.bind_tools(tools)
