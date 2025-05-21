from langchain.tools import StructuredTool
from piragua_chat.services.physicochemical_service import (
    get_last_water_quality_measurement,
)

get_last_water_quality_tool = StructuredTool.from_function(
    func=get_last_water_quality_measurement,
    name="ultima_medicion_calidad_agua",
    description="""Consulta la última medición de calidad en un punto de monitoreo y muestra un resumen de los parámetros:
    Conductividad eléctrica, Oxígeno Disuelto, Porcentaje de Saturación de Oxigeno.
    """,
)
