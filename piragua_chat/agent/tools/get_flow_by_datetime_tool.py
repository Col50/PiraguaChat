from langchain.tools import StructuredTool

from piragua_chat.services.stream_gage_service import get_flow_by_datetime


get_flow_by_datetime_tool = StructuredTool.from_function(
    func=get_flow_by_datetime,
    name="consultar_caudal_por_fecha_hora",
    description="""Consulta el caudal registrado en una estación en una fecha y hora específica.
    Parámetros:
        station_id: código de la estación (int)
        date_string: string en formato 'YYYY-MM-DD'
        time: string en formato 'HH' (hora en 24h, ej: '10' para 10am)
    Retorna el valor de caudal y nivel para esa fecha y hora exacta.
    """,
)
