from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import logging
import requests

# Importa el runner del agente desde tu nueva estructura

logger = logging.getLogger(__name__)

from piragua_chat.models.history_message import Historial_Mensaje
from piragua_chat.views.langchain_agent_view import (
    handle_agent_query,
)  # Importar la función reutilizable


class WhatsAppWebhookView(APIView):
    def post(self, request):
        from_number = request.data.get("From", "")
        body = request.data.get("Body", "").strip()

        logger.info(f"Mensaje de WhatsApp recibido: {from_number} - {body}")

        try:
            # Guardar el mensaje del usuario en la base de datos
            Historial_Mensaje.objects.create(
                numero_celular=from_number,
                tipo_usuario="persona",
                mensaje=body,
            )

            # Llamar directamente a la lógica del agente
            result = handle_agent_query(body, from_number)

            # Guardar la respuesta generada por la IA en la base de datos
            Historial_Mensaje.objects.create(
                numero_celular=from_number,
                tipo_usuario="ai",
                mensaje=result,
            )

        except Exception as e:
            result = f"Error al procesar la consulta: {str(e)}"

        return Response({"reply": result}, status=status.HTTP_200_OK)
