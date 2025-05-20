from langchain.tools import StructuredTool
from piragua_chat.services.meteorological_station_service import (
    get_max_precipitation_event_by_municipality,
)

max_precipitation_event_tool = StructuredTool.from_function(
    func=get_max_precipitation_event_by_municipality,
    name="evento_maximo_precipitacion_municipio",
    description="""Devuelve el evento de precipitación más fuerte registrado en cualquier estación meteorológica de un municipio.
    Requiere el nombre del municipio como parámetro.
    """,
)
