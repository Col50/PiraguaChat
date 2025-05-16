from langchain.tools import StructuredTool
from piragua_chat.services.documents_service import get_document

get_document_tool = StructuredTool.from_function(
    func=get_document,
    name="buscar_documentos_func",
    description="Busca documentos por palabras clave y opcionalmente por año.",
)
