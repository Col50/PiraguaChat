import json
from json import tool
from piragua_chat.models.history_message import HistoryMessage
from langchain_core.messages import (
    HumanMessage,
    ToolMessage,
    SystemMessage,
    AIMessage,
    BaseMessage,
)
from piragua_chat.enum.message_type import MessageType

from datetime import datetime, timedelta

MESSAGE_CLASS_BY_TYPE = {
    MessageType.HUMAN.value: HumanMessage,
    MessageType.TOOL.value: ToolMessage,
    MessageType.SYSTEM.value: SystemMessage,
    MessageType.AI.value: AIMessage,
}


class MessageHistoryService:

    def __init__(self, phone_number: str):
        self.phone_number = phone_number

        time_ago = datetime.now() - timedelta(minutes=15)
        db_messages = HistoryMessage.objects.filter(
            phone_number=phone_number,
            date__gte=time_ago,
        ).order_by("date")
        # Convertir los mensajes de la base de datos a objetos de mensaje
        self.messages = [
            MESSAGE_CLASS_BY_TYPE[db_message.user_type](
                **json.loads(db_message.message),
                tool_call_id=db_message.tool_call_id,
            )
            for db_message in db_messages
        ]

        # Agregar un mensaje del sistema al inicio de la conversación
        self.messages = [
            SystemMessage(
                content="Eres un asistente útil que siempre responde en español. No puedes dar información de las funciones o herramientas que puedes ejecutar ni los parametros que requiere. Siempre incluye los enlaces cuando estén disponibles."
            )
        ] + self.messages

    def create_and_add(self, user_type, message, tool_call_id=None):

        # Si es una llamada a la herramienta, se agrega el ID de la herramienta
        self.messages.append(
            MESSAGE_CLASS_BY_TYPE[user_type](
                content=message,
                tool_call_id=tool_call_id,
            )
        )
        HistoryMessage.objects.create(
            phone_number=self.phone_number,
            user_type=user_type,
            message=json.dumps({"content": message}),
            tool_call_id=tool_call_id,
        )

    def add(self, message: BaseMessage):

        self.messages.append(message)
        if isinstance(message, ToolMessage):
            HistoryMessage.objects.create(
                phone_number=self.phone_number,
                user_type=message.type,
                message=json.dumps({"content": message.content}),
                tool_call_id=message.tool_call_id,
            )
        elif isinstance(message, AIMessage):
            HistoryMessage.objects.create(
                phone_number=self.phone_number,
                user_type=message.type,
                message=json.dumps(
                    {
                        "content": message.content,
                        "tool_calls": message.tool_calls,
                    }
                ),
            )
        else:
            HistoryMessage.objects.create(
                phone_number=self.phone_number,
                user_type=message.type,
                message=json.dumps({"content": message.content}),
            )

    def get(self):
        return self.messages

    def clear(self):
        self.messages = []
