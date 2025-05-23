import os
from dotenv import load_dotenv

from piragua_chat.agent.tools.get_municipalities_tool import get_municipalities_tool
from piragua_chat.agent.tools.get_document_tool import get_document_tool
from piragua_chat.agent.tools.get_physicochemical_report_tool import (
    get_physicochemical_report_tool,
)
from piragua_chat.agent.tools.get_hydrobiological_report_tool import (
    get_hydrobiological_report_tool,
)
from piragua_chat.agent.tools.get_todays_date_tool import get_todays_date_tool
from piragua_chat.agent.tools.get_faqs_tool import get_faqs_tool
from piragua_chat.agent.tools.get_limnigraphy_tool import get_limnigraphy_tool
from piragua_chat.agent.tools.get_territories_tool import get_territories_tool
from piragua_chat.agent.tools.get_weather_station_tool import get_weather_station_tool
from piragua_chat.agent.tools.get_max_flow_by_source_tool import (
    get_max_flow_by_source_tool,
)
from piragua_chat.agent.tools.get_min_flow_by_source_tool import (
    get_min_flow_by_source_tool,
)
from piragua_chat.agent.tools.get_thresholds_count_tool import get_thresholds_count_tool
from piragua_chat.agent.tools.get_max_precipitation_event_by_municipality_tool import (
    get_max_precipitation_event_by_municipality_tool,
)

from piragua_chat.agent.tools.get_rain_level_by_datetime_tool import (
    get_rain_level_by_datetime_tool,
)
from piragua_chat.agent.tools.get_flow_by_datetime_tool import get_flow_by_datetime_tool
from piragua_chat.agent.tools.get_water_quality import get_water_quality_tool
from piragua_chat.agent.tools.get_last_water_quality_tool import (
    get_last_water_quality_measurement_tool,
)
from piragua_chat.agent.tools.get_monitored_water_sources_tool import (
    get_monitored_water_sources_tool,
)
from piragua_chat.agent.tools.get_monitoring_points_location_tool import (
    get_monitoring_points_location_tool,
)
from piragua_chat.agent.tools.get_monitored_sources_count_tool import (
    get_monitored_sources_count_tool,
)
from piragua_chat.agent.tools.get_training_name_service_tool import (
    get_training_name_tool,
)

from piragua_chat.agent.tools.get_station_count_by_type_tool import (
    get_station_count_by_type_tool,
)

from piragua_chat.agent.tools.get_activities_by_municipality_tool import (
    get_activities_by_municipality_tool,
)

from langchain_openai import ChatOpenAI

from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# === Tools ===
tools = [
    get_document_tool,
    get_physicochemical_report_tool,
    get_hydrobiological_report_tool,
    get_todays_date_tool,
    get_faqs_tool,
    get_municipalities_tool,
    get_territories_tool,
    get_limnigraphy_tool,
    get_max_flow_by_source_tool,
    get_min_flow_by_source_tool,
    get_weather_station_tool,
    get_thresholds_count_tool,
    get_max_precipitation_event_by_municipality_tool,
    get_rain_level_by_datetime_tool,
    get_flow_by_datetime_tool,
    get_water_quality_tool,
    get_last_water_quality_measurement_tool,
    get_monitored_water_sources_tool,
    get_monitoring_points_location_tool,
    get_monitored_sources_count_tool,
    get_station_count_by_type_tool,
    get_training_name_tool,
    get_activities_by_municipality_tool,
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
