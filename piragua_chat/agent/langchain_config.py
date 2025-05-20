import os
from dotenv import load_dotenv

from piragua_chat.agent.tools.get_municipality_tool import get_municipality_tool
from piragua_chat.agent.tools.get_document_tool import get_document_tool
from piragua_chat.agent.tools.get_physicochemical_report_tool import (
    get_physicochemical_report_tool,
)
from piragua_chat.agent.tools.get_hydrobiological_report_tool import (
    get_hydrobiological_report_tool,
)
from piragua_chat.agent.tools.get_todays_date_tool import get_todays_date_tool
from piragua_chat.agent.tools.get_faq_tool import get_faq_tool
from piragua_chat.agent.tools.get_limnigraphy_tool import get_limnigraphy_tool
from piragua_chat.agent.tools.get_territorial_tool import get_territorial_tool
from piragua_chat.agent.tools.get_weather_station_tool import get_weather_station_tool
from piragua_chat.agent.tools.get_max_flow_tool import get_max_flow_tool
from piragua_chat.agent.tools.get_min_flow_tool import get_min_flow_tool
from piragua_chat.agent.tools.count_thresholds_tool import count_thresholds_tool
from piragua_chat.agent.tools.max_precipitation_event_tool import (
    max_precipitation_event_tool,
)
from piragua_chat.agent.tools.rain_by_datetime_tool import rain_by_datetime_tool
from piragua_chat.agent.tools.flow_by_datetime_tool import flow_by_datetime_tool


from langchain_openai import ChatOpenAI

from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# === Tools ===
tools = [
    get_document_tool,
    get_physicochemical_report_tool,
    get_hydrobiological_report_tool,
    get_todays_date_tool,
    get_faq_tool,
    get_municipality_tool,
    get_territorial_tool,
    get_limnigraphy_tool,
    get_max_flow_tool,
    get_min_flow_tool,
    get_weather_station_tool,
    count_thresholds_tool,
    max_precipitation_event_tool,
    rain_by_datetime_tool,
    flow_by_datetime_tool,
]

# tool_list = {tool.name: tool for tool in tools}

# llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-pro-latest",
#     api_key=os.getenv("GENAI_API_KEY"),
#     temperature=0.3,
# )

# llm_with_tools = llm.bind_tools(tools)


tool_list = {tool.name: tool for tool in tools}

llm = ChatOpenAI(
    model="gpt-4",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.3,
)

llm_with_tools = llm.bind_tools(tools)
