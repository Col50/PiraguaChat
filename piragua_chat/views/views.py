from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import logging

# Importa el runner del agente desde tu nueva estructura
from piragua_chat.agent.agent_runner import process_query

logger = logging.getLogger(__name__)


class LangchainAgentView(APIView):
    def post(self, request, *args, **kwargs):
        logger.info("Mensaje recibido: %s", request.data)

        query = request.data.get("query", "")
        if not query:
            return Response(
                {"error": "No se recibió ninguna consulta."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            result = process_query(query)
            return Response({"response": result}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Error en el agente LangChain: %s", str(e))
            return Response(
                {
                    "error": "Ocurrió un error interno. Por favor, inténtelo de nuevo más tarde."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
