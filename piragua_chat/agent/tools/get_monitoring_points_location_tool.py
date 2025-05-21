from langchain.tools import StructuredTool
from piragua_chat.services.monitored_sources_service import (
    get_monitoring_points_location,
)

get_monitoring_points_location_tool = StructuredTool.from_function(
    func=get_monitoring_points_location,
    name="ubicacion_puntos_monitoreo_municipio",
    description="""Devuelve la ubicación (altitud, longitud, latitud) de los puntos de monitoreo en el municipio especificado por el usuario.""",
)
