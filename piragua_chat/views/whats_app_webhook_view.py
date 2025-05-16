from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import logging
import requests

from piragua_chat.agent.agent_runner import process_query

# Importa el runner del agente desde tu nueva estructura

logger = logging.getLogger(__name__)

from piragua_chat.models.history_message import HistoryMessage
from piragua_chat.views.langchain_agent_view import (
    handle_agent_query,
)  # Importar la función reutilizable

from piragua_chat.services.message_history_service import (
    MessageHistoryService,
)  # Asumiendo que ahí defines la clase


class WhatsAppWebhookView(APIView):
    def post(self, request):
        phone_number = request.data.get("From", "")
        body = request.data.get("Body", "").strip()

        logger.info(f"Mensaje de WhatsApp recibido: {phone_number} - {body}")

        try:
            # Guardar el mensaje del usuario en la base de datos
            message_history = MessageHistoryService(phone_number)

            # Llamar directamente a la lógica del agente
            result = process_query(body, message_history)

            # Guardar la respuesta generada por la IA en la base de datos

        except Exception as e:
            result = f"Error al procesar la consulta: {str(e)}"

        return Response({"reply": result}, status=status.HTTP_200_OK)
