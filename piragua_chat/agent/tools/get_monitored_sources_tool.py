from langchain.tools import StructuredTool
from piragua_chat.services.monitored_sources_service import (
    get_monitored_sources,
)

get_monitored_sources_tool = StructuredTool.from_function(
    func=get_monitored_sources,
    name="fuentes_monitoreadas_municipio",
    description="""Devuelve la lista de fuentes (quebradas/ríos) que se monitorean en el municipio especificado por el usuario.
    Requiere el nombre del municipio como parámetro.
    """,
)
