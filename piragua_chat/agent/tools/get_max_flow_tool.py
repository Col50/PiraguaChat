from langchain.tools import StructuredTool
from piragua_chat.services.get_max_flow_service import get_max_flow_by_source

get_max_flow_tool = StructuredTool.from_function(
    func=get_max_flow_by_source,
    name="consultar_caudal_maximo_fuente",
    description="""Consulta el caudal máximo registrado en una fuente hídrica (río o quebrada). 
        Requiere el parámetro source_name (str) con el nombre de la fuente.
        El nombre de la fuentepuede varirar las mayusculas, minusculas y acentos.""",
)
