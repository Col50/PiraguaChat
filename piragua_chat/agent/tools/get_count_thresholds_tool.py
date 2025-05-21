from langchain.tools import StructuredTool
from piragua_chat.services.threshold_count_service import (
    count_thresholds_by_municipality,
)

get_count_thresholds_tool = StructuredTool.from_function(
    func=count_thresholds_by_municipality,
    name="contar_umbrales_municipio",
    description="""Cuenta cuántos umbrales (ROJO, NARANJA, AMARILLO) se han reportado en todos los puntos de monitoreo de un municipio.
    Requiere el nombre del municipio y el tipo de umbral (ROJO, NARANJA o AMARILLO).
    """,
)
