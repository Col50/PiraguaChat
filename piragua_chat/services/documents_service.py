import os
import requests
from typing import Optional


def get_document(
    searchString: Optional[str] = None, year: Optional[int] = None
) -> dict:
    base_url = f'{os.getenv("BASE_API_URL")}/documentos'

    params = {}
    if searchString:
        params["search"] = searchString.strip().strip('"').strip("'")
    if year:
        params["search"] = year

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return {"resultados": response.json().get("values", [])}
    except requests.RequestException as e:
        return f"Error al buscar documentos: {e}"
