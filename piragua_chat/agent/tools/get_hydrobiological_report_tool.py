from langchain.tools import StructuredTool
from piragua_chat.services.hydrobiological_service import get_hydrobiological_report

get_hydrobiological_report_tool = StructuredTool.from_function(
    func=get_hydrobiological_report,
    name="descargar_reporte_hidrobiologico",
    description="Devuelve el enlace de descarga del reporte hidrobiológico.",
)
