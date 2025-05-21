from langchain.tools import StructuredTool
from piragua_chat.services.station_count_by_type_service import (
    get_station_count_by_type,
)

get_station_count_by_type_tool = StructuredTool.from_function(
    func=get_station_count_by_type,
    name="contar_estaciones_por_tipo_municipio",
    description="""Devuelve la cantidad de estaciones de un tipo específico (pluviográficas, limnigráficas, meteorológicas o piezómetros) en el municipio indicado.
        tipo_nombre: tipo de estación (puede ser 'pluviográfica', 'limnigráfica', 'meteorológica', 'piezómetro' o palabras relacionadas)
    """,
)
