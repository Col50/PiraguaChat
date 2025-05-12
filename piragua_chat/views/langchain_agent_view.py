from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import logging

# Importa el runner del agente desde tu nueva estructura
from piragua_chat.agent.agent_runner import process_query

from piragua_chat.models.history_message import Historial_Mensaje
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


def handle_agent_query(query, from_number):
    """
    Maneja la lógica principal del agente LangChain.
    """
    try:
        # Obtener mensajes del mismo número de celular en los últimos 15 minutos
        time_ago = datetime.now() - timedelta(minutes=15)
        recent_history = Historial_Mensaje.objects.filter(
            numero_celular=from_number,
            hora__gte=time_ago,
        ).order_by("hora")

        # Construir el contexto a partir del historial reciente
        contexto = "\n".join(
            [f"{mensaje.tipo_usuario}: {mensaje.mensaje}" for mensaje in recent_history]
        )
        # Agregar el contexto al query
        query_con_contexto = f"{contexto}\nUsuario: {query}"
        # Procesar la consulta con el contexto
        result = process_query(query_con_contexto)
        return result
    except Exception as e:
        logger.error("Error en el agente LangChain: %s", str(e))
        raise e


class LangchainAgentView(APIView):
    def post(self, request, *args, **kwargs):
        logger.info("Mensaje recibido: %s", request.data)
        query = request.data.get("query", "")
        from_number = request.data.get("from_number", "")
        if not query:
            return Response(
                {"error": "No se recibió ninguna consulta."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            result = handle_agent_query(query, from_number)
            return Response({"response": result}, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {
                    "error": "Ocurrió un error interno. Por favor, inténtelo de nuevo más tarde."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
