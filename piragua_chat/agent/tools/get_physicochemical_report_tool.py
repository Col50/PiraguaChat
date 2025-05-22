from langchain.tools import StructuredTool
from piragua_chat.services.physicochemical_service import get_physicochemical_report

get_physicochemical_report_tool = StructuredTool.from_function(
    func=get_physicochemical_report,
    name="descargar_reporte_fisicoquimicos",
    description="Devuelve el enlace de descarga del reporte físico-químico.",
)
