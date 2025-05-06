import os
import requests
from typing import Optional


def get_document(titulo: Optional[str] = None, año: Optional[int] = None) -> dict:
    base_url = os.getenv("DOCUMENT_API")
    if not base_url:
        raise ValueError("La variable de entorno 'DOCUMENT_API' no está definida.")

    params = {}
    if titulo:
        params["search"] = titulo.strip().strip('"').strip("'")
    if año:
        params["search"] = año

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return {"resultados": response.json().get("values", [])}
    except requests.RequestException as e:
        return f"Error al buscar documentos: {e}"
