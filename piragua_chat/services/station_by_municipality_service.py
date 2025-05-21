import os
import requests


def get_station_codes_by_municipality(municipality_id: str, type: str = None) -> list:
    """
    Retorna una lista de códigos de estaciones para un municipio dado.
    Si se especifica 'tipo', filtra por el tipo de estación (por ejemplo, 'meteorologica').
    """
    stations_url = f'{os.getenv("BASE_API_URL")}/estaciones'
    try:
        resp = requests.get(
            stations_url, params={"municipio": municipality_id, "tipo": type}
        )
        resp.raise_for_status()
        stations = resp.json().get("values", [])
        return [est.get("codigo") for est in stations if est.get("codigo")]
    except requests.RequestException:
        return []
