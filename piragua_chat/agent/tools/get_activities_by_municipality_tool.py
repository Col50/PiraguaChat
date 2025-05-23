from langchain.tools import StructuredTool
from piragua_chat.services.activity_service import (
    get_activities_by_municipality,
)

get_activities_by_municipality_tool = StructuredTool.from_function(
    func=get_activities_by_municipality,
    name="actividades_en_municipio",
    description="""Devuelve las actividades realizadas en el municipio especificado, consultando los grupos piragueros y sus asistencias.
    Parámetro:
        municipality_name: nombre del municipio
    """,
)
