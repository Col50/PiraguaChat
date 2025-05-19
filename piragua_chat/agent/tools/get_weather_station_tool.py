from langchain.tools import StructuredTool
from piragua_chat.services.weather_station_service import get_last_weather_station

get_weather_station_tool = StructuredTool.from_function(
    func=get_last_weather_station,
    name="consultar_meteorologia_estacion",
    description="""Consulta el registro meteorologia de una estación meteorologica, en la cual puede consultar la presipitacion (lluvia) registrada.
        Requiere el parámetro station_id correspondiente al ID de la estación.
        Puede consultar el ultimo registro de la estacion meteorologica
        Convierte el formato de fecha a (UTC-5)
        """,
)
