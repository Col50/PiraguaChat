from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import logging
import requests

# Importa el runner del agente desde tu nueva estructura

logger = logging.getLogger(__name__)

from piragua_chat.models.history_message import Historial_Mensaje


# class WhatsAppWebhookView(APIView):
#     def post(self, request):
#         from_number = request.data.get("From", "")
#         print(f"----------------------from_number: {from_number}")
#         body = request.data.get("Body", "").strip()
#         num_media = int(request.data.get("NumMedia", 0))

#         logger.info(f"Mensaje de WhatsApp recibido: {from_number} - {body}")
#         print(f"Mensaje de WhatsApp recibido: {from_number} - {body}")

#         print(f"----------------------num_media: {num_media}")

#         query_data = {"query": body}
#         query_url = "http://localhost:8000/agent/"

#         try:

#             # Guardar el mensaje del usuario en la base de datos
#             Historial_Mensaje.objects.create(
#                 numero_celular=from_number,
#                 tipo_usuario="persona",
#                 mensaje=body,
#             )

#             response = requests.post(query_url, json=query_data)
#             print(f"Respuesta cruda de /query/: {response.text}")

#             try:
#                 response_data = response.json()
#                 if response.status_code == 200:
#                     result = response_data.get(
#                         "response", "No se pudo obtener respuesta."
#                     )
#                 else:
#                     result = "Error al procesar la consulta."
#             except Exception as parse_error:
#                 result = f"Error al interpretar respuesta JSON: {parse_error}"

#         except Exception as e:
#             result = f"Error al contactar el servidor de consultas: {str(e)}"

#             # twiml_response.message(result)

#         # print("Respuesta que se enviará a Twilio:", str(twiml_response))
#         # return HttpResponse(str(twiml_response), content_type="application/xml")
#         return Response({"reply": result}, status=status.HTTP_200_OK)


class WhatsAppWebhookView(APIView):
    def post(self, request):
        from_number = request.data.get("From", "")
        body = request.data.get("Body", "").strip()
        num_media = int(request.data.get("NumMedia", 0))

        logger.info(f"Mensaje de WhatsApp recibido: {from_number} - {body}")

        query_data = {"query": body}
        query_url = "http://localhost:8000/agent/"

        try:
            # Guardar el mensaje del usuario en la base de datos
            Historial_Mensaje.objects.create(
                numero_celular=from_number,
                tipo_usuario="persona",
                mensaje=body,
            )

            # Enviar la consulta al agente
            response = requests.post(query_url, json=query_data)
            response_data = response.json()
            if response.status_code == 200:
                result = response_data.get("response", "No se pudo obtener respuesta.")
            else:
                result = "Error al procesar la consulta."

            # Guardar la respuesta generada por la IA en la base de datos
            Historial_Mensaje.objects.create(
                numero_celular=from_number,
                tipo_usuario="ai",
                mensaje=result,
            )

        except Exception as e:
            result = f"Error al contactar el servidor de consultas: {str(e)}"

        return Response({"reply": result}, status=status.HTTP_200_OK)
