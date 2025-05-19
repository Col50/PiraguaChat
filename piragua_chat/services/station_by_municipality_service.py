import os
import requests


def get_station_codes_by_municipality(municipio_id: str, tipo: str = None) -> list:
    """
    Retorna una lista de códigos de estaciones para un municipio dado.
    Si se especifica 'tipo', filtra por el tipo de estación (por ejemplo, 'meteorologica').
    """
    estaciones_url = f'{os.getenv("BASE_API_URL")}/estaciones'
    try:
        resp = requests.get(estaciones_url, params={"municipio": municipio_id})
        resp.raise_for_status()
        estaciones = resp.json().get("values", [])
        return [est.get("codigo") for est in estaciones if est.get("codigo")]
    except requests.RequestException:
        return []
