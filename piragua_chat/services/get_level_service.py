import os
import requests


def get_limnigraphy(station_id: int) -> dict:
    base_url = f'{os.getenv("BASE_API_URL")}/estaciones/{station_id}/nivel'
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        values = response.json().get("values", [])
        if not values:
            return {"error": "No se encontraron registros para la estación."}
        latest = values[0]  # El primer registro es el más reciente
        return {
            "fecha": latest.get("fecha"),
            "caudal": latest.get("caudal"),
            "nivel": latest.get("nivel"),
            "id": latest.get("id"),
        }
    except requests.RequestException:
        return {"error": "Error al consultar los datos de nivel de la estación."}
