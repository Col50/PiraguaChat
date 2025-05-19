import os
import requests


def get_faq(question: str) -> dict:
    """
    Devuelve la lista de preguntas frecuentes y sus respuestas.
    El LLM debe seleccionar la respuesta más relevante según la pregunta del usuario.
    """
    base_url = f'{os.getenv("BASE_API_URL")}/faqs'
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        faqs = response.json().get("values", [])
        return {"faqs": faqs}
    except requests.RequestException as e:
        return f"Error al consultar las preguntas frecuentes"
