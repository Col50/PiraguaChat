from rest_framework.views import APIView

import os
import requests
from django.http import JsonResponse
from rest_framework.views import APIView

from django.conf import settings
from piragua_chat.services.ocr_google_service import get_handwritten_text_from_image
from piragua_chat.services.ocr_aws_service import get_handwritten_text_from_image_aws


IMAGES_DIR = os.path.join(settings.BASE_DIR, "imagenes")
os.makedirs(IMAGES_DIR, exist_ok=True)


class WhatsAppOCRView(APIView):
    print("WhatsAppOCRView initialized")

    def post(self, request):
        body = request.data.get("url", "").strip()
        print("Received request:")
        print(f"Body received: {body}")  # Para ver lo que llega

        data = request.POST or request.data or request.body
        print("Data received:", data)
        # Try to get JSON body if possible
        try:
            import json

            if isinstance(data, bytes):
                data = json.loads(data.decode())
            elif hasattr(data, "get"):
                data = data
            else:
                data = json.loads(data)
        except Exception:
            return JsonResponse({"error": "Invalid JSON body"}, status=400)

        image_url = data.get("url")
        if not image_url:
            return JsonResponse({"error": "Missing 'url' in body"}, status=400)

        try:
            response = requests.get(image_url)
            if response.status_code != 200:
                return JsonResponse({"error": "Failed to download image"}, status=400)
            filename = os.path.basename(image_url.split("?")[0])
            file_path = os.path.join(IMAGES_DIR, filename)
            with open(file_path, "wb") as f:
                f.write(response.content)
        except Exception as e:
            return JsonResponse(
                {"error": f"Error downloading image: {str(e)}"}, status=500
            )

        # text = get_handwritten_text_from_image(file_path)
        text = get_handwritten_text_from_image_aws(file_path)

        if text is None:
            return JsonResponse({"error": "OCR failed"}, status=500)
        return JsonResponse({"text": text})
