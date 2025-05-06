from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from .langchain_config import llm_with_tools, tool_list

system_message = SystemMessage(
    content="Eres un asistente útil que siempre responde en español, sin mencionar que se usan herramientas. Siempre incluye los enlaces cuando estén disponibles."
)


def process_query(query: str) -> str:
    try:
        messages = [system_message, HumanMessage(content=query)]

        for _ in range(3):  # máximo 3 ciclos
            ai_message = llm_with_tools.invoke(messages)
            messages.append(ai_message)

            if not ai_message.tool_calls:
                return ai_message.content

            for tool_call in ai_message.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_id = tool_call["id"]

                selected_tool = tool_list.get(tool_name)
                if not selected_tool:
                    return f"⚠️ Herramienta no encontrada: {tool_name}"

                tool_output = selected_tool.invoke(tool_args)
                messages.append(
                    ToolMessage(content=str(tool_output), tool_call_id=tool_id)
                )

        final_message = llm_with_tools.invoke(messages)
        return final_message.content

    except Exception as e:
        return f"Error al ejecutar el agente: {str(e)}"
