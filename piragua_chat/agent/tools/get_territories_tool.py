from langchain.tools import StructuredTool
from piragua_chat.services.territorial_service import get_territories

get_territories_tool = StructuredTool.from_function(
    func=get_territories,
    name="adquirir_territorios",
    description=""" Puedes descargar toda la lista de los territorios en los cuales tiene cobertura el proyecto Piragua.""",
)
