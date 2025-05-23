from langchain.tools import StructuredTool
from piragua_chat.services.stream_gage_service import get_min_flow_by_source

get_min_flow_by_source_tool = StructuredTool.from_function(
    func=get_min_flow_by_source,
    name="consultar_caudal_minimo_fuente",
    description="""Consulta el caudal minimo registrado en una fuente hídrica (río o quebrada). 
         Requiere el parámetro source_name con el nombre de la fuente.""",
)
