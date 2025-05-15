from langchain.tools import StructuredTool
from piragua_chat.services.faqs_service import get_faq

get_faq_tool = StructuredTool.from_function(
    func=get_faq,
    name="buscar_pregunta_frecuente",
    description=(
        "Busca en la lista de preguntas frecuentes de Piragua y selecciona la respuesta más relevante "
        "según la pregunta del usuario. Devuelve solo la respuesta más adecuada, aunque la pregunta del usuario "
        "no coincida exactamente con ninguna FAQ."
    ),
)
