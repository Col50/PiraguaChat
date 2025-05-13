from email import message
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage

from piragua_chat.services.message_history_service import MessageHistoryService
from .langchain_config import llm_with_tools, tool_list


def process_query(query: str, message_history: MessageHistoryService) -> str:

    try:
        message_history.create_and_add("human", query)
        for _ in range(3):  # máximo 3 ciclos
            ai_message = llm_with_tools.invoke(message_history.get())

            message_history.add(ai_message)

            # print("ai_message.tool_calls-----", ai_message.tool_calls)
            print("message_history.get()------", message_history.get())
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
                message_history.create_and_add(
                    "tool", str(tool_output), tool_call_id=tool_id
                )

        final_message = llm_with_tools.invoke(message_history.get())

        return final_message.content

    except Exception as e:
        return f"Error al ejecutar el agente: {str(e)}"
