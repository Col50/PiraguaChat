from langchain.tools import StructuredTool
from piragua_chat.services.municipality_service import get_municipalities

get_municipalities_tool = StructuredTool.from_function(
    func=get_municipalities,
    name="adquirir_municipios",
    description=""" Puedes descargar toda la lista de los municipios en los cuales tiene cobertura el proyecto Piragua.""",
)
