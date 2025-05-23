from langchain.tools import StructuredTool
from piragua_chat.services.monitored_sources_service import (
    get_monitored_sources_count,
)

get_monitored_sources_count_tool = StructuredTool.from_function(
    func=get_monitored_sources_count,
    name="conteo_fuentes_monitoreadas_municipio",
    description="""Devuelve el conteo de puntos de monitoreo en el municipio especificado por el usuario.""",
)
