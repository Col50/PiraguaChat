import os
from dotenv import load_dotenv
from langchain.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from piragua_chat.services.documents import get_document
from piragua_chat.services.physicochemical import get_physicochemical_report
from piragua_chat.services.hydrobiological import get_hydrobiological_report
from piragua_chat.services.date import get_todays_date

load_dotenv()

# === Tools ===
get_document_tool = StructuredTool.from_function(
    func=get_document,
    name="buscar_documentos_func",
    description="Busca documentos por título y opcionalmente por año.",
)

get_physicochemical_report_tool = StructuredTool.from_function(
    func=get_physicochemical_report,
    name="descargar_reporte_fisicoquimicos",
    description="Devuelve el enlace de descarga del reporte físico-químico.",
)

get_hydrobiological_report_tool = StructuredTool.from_function(
    func=get_hydrobiological_report,
    name="descargar_reporte_hidrobiologico",
    description="Devuelve el enlace de descarga del reporte hidrobiológico.",
)

get_todays_date_tool = StructuredTool.from_function(
    func=get_todays_date,
    name="obtener_fecha_hoy",
    description="Devuelve la fecha y el día actual.",
)

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
