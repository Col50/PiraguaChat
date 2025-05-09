from langchain.tools import StructuredTool
from piragua_chat.services.date import get_todays_date

get_todays_date_tool = StructuredTool.from_function(
    func=get_todays_date,
    name="obtener_fecha_hoy",
    description="Devuelve la fecha y el día actual.",
)
