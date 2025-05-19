import os
import requests


def get_weather_station(station_id: int) -> dict:
    base_url = f'{os.getenv("BASE_API_URL")}/estaciones/{station_id}/meteorologia'
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        values = response.json().get("values", [])
        if not values:
            return {"error": "No se encontraron registros para la estación."}
        latest = values[0]
        return {
            "fecha": latest.get("fecha"),
            "lluvia": latest.get("lluvia"),
            "id": latest.get("id"),
        }
    except requests.RequestException:
        return {"error": "Error al consultar los datos de la estación."}
