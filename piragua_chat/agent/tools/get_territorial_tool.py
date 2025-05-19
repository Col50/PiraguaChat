from langchain.tools import StructuredTool
from piragua_chat.services.get_territorial_service import get_territorial

get_territorial_tool = StructuredTool.from_function(
    func=get_territorial,
    name="buscar_territorio",
    description=""" Puedes descargar toda la lista de los territorios en los cuales tiene cobertura el proyecto Piragua.""",
)
