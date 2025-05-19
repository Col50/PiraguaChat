import os
import requests


def get_last_weather_station(station_id: int) -> dict:
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


def get_all_weather_station_records(station_ids) -> dict:
    """
    Retorna todos los registros meteorológicos de una o varias estaciones.
    Si una estación falla, continúa con las demás.
    Retorna un diccionario {station_id: [registros]}.
    """
    if not isinstance(station_ids, list):
        station_ids = [station_ids]
    results = {}
    for station_id in station_ids:
        print(f"------Consultando la estación meteorológica: {station_id}")
        base_url = f'{os.getenv("BASE_API_URL")}/estaciones/{station_id}/meteorologia'
        try:
            response = requests.get(base_url)
            response.raise_for_status()
            values = response.json().get("values", [])
            results[station_id] = values
        except requests.RequestException:
            results[station_id] = []
    return results
