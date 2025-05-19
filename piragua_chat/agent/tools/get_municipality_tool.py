from langchain.tools import StructuredTool
from piragua_chat.services.municipality_service import get_municipality

get_municipality_tool = StructuredTool.from_function(
    func=get_municipality,
    name="buscar_municipio",
    description=""" Puedes descargar toda la lista de los municipios en los cuales tiene cobertura el proyecto Piragua.""",
)
