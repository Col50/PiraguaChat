from langchain.tools import StructuredTool
from piragua_chat.services.training_service import get_training_name

get_training_name_tool = StructuredTool.from_function(
    func=get_training_name,
    name="buscar_formaciones",
    description=""" Puedes descargar toda la lista de formación se ofrecen a las comunidades.""",
)
