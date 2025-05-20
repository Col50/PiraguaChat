from langchain.tools import StructuredTool
from piragua_chat.services.physicochemical_service import (
    get_water_quality,
)

get_min_flow_tool = StructuredTool.from_function(
    func=get_water_quality,
    name="consultar_calidad_fuente_agua",
    description="""Retorna los resultados del indice de calidad de agua (ICA). 
                para todos los monitoreos fisicoquímicos .""",
)
