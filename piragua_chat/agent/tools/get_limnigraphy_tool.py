from langchain.tools import StructuredTool
from piragua_chat.services.get_limnigraphy_service import get_limnigraphy

get_limnigraphy_tool = StructuredTool.from_function(
    func=get_limnigraphy,
    name="consultar_nivel_estacion",
    description="""Consulta el registro de nivel y caudal de una estación automática limnigráfica.
        Requiere el parámetro station_id correspondiente al ID de la estación.
        Puede consultar el ultimo registro de la estacion limnigráfica
        Convierte el formato de fecha a (UTC-5)
        """,
)
