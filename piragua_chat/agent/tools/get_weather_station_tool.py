from langchain.tools import StructuredTool
from piragua_chat.services.meteorological_station_service import (
    get_meteorological_station,
)

get_weather_station_tool = StructuredTool.from_function(
    func=get_meteorological_station,
    name="consultar_meteorologia_estacion",
    description="""Consulta el registro meteorologia de una estación meteorologica, en la cual puede consultar la presipitacion (lluvia) registrada.
        Puede consultar el ultimo registro de la estacion meteorologica
        convierte el formato de fecha a (UTC-5)
        """,
)
