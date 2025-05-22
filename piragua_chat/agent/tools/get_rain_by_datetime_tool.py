from langchain.tools import StructuredTool
from piragua_chat.services.meteorological_station_service import get_rain_by_datetime


get_rain_by_datetime_tool = StructuredTool.from_function(
    func=get_rain_by_datetime,
    name="consultar_lluvia_por_fecha_hora",
    description="""Consulta el nivel de lluvia registrado en una estación meteorológica en una fecha y hora específica.
    Parámetros:
        station_id: código de la estación (int)
        date_string: string en formato 'YYYY-MM-DD'
        time: string en formato 'HH' (hora en 24h, ej: '10' para 10am)
    Retorna el valor de lluvia para esa fecha y hora exacta.
    """,
)
