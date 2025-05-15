from langchain.tools import StructuredTool
from piragua_chat.services.faqs_service import get_faq

get_faq_tool = StructuredTool.from_function(
    func=get_faq,
    name="buscar_pregunta_frecuente",
    description="Busca una respuesta en las preguntas frecuentes de Piragua a partir de una pregunta del usuario.",
)
