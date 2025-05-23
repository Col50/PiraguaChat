import os
import requests


def get_faqs(question: str) -> dict:
    base_url = f'{os.getenv("BASE_API_URL")}/faqs'
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        faqs = response.json().get("values", [])
        return {"faqs": faqs}
    except requests.RequestException as e:
        return f"Error al consultar las preguntas frecuentes"
