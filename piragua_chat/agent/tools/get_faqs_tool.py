from langchain.tools import StructuredTool
from piragua_chat.services.faqs_service import get_faqs

get_faqs_tool = StructuredTool.from_function(
    func=get_faqs,
    name="buscar_pregunta_frecuente",
    description=""" Puedes descargar toda la lista de preguntas frecuentes de Piragua y sus respuestas.""",
)
