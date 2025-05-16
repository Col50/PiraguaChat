from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
from piragua_chat.agent.agent_runner import process_query

logger = logging.getLogger(__name__)

from piragua_chat.services.message_history_service import (
    MessageHistoryService,
)


class WhatsAppWebhookView(APIView):
    def post(self, request):
        phone_number = request.data.get("From", "")
        body = request.data.get("Body", "").strip()

        logger.info(f"Mensaje de WhatsApp recibido: {phone_number} - {body}")

        try:
            #  Recupera el historial almacenado en la base de datos
            message_history = MessageHistoryService(phone_number)

            # Llamar directamente a la lógica del agente
            result = process_query(body, message_history)

        except Exception as e:
            result = f"Error al procesar la consulta: {str(e)}"

        return Response({"reply": result}, status=status.HTTP_200_OK)
