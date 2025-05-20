import os
import requests
from piragua_chat.services.normalize_text_service import normalize_text


def get_station_code_by_water_monitoring_name(source_name: str) -> list:
    """
    Busca todos los códigos de estaciones de monitoreo aguas subterraneas por nombre.
    """
    base_url = f'{os.getenv("BASE_API_URL")}/subterraneas'
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        estaciones = response.json().get("values", [])
        source_name_normalized = normalize_text(source_name)
        codes = [
            est.get("codigo")
            for est in estaciones
            if normalize_text(est.get("fuente", "")) == source_name_normalized
        ]
        return codes
    except requests.RequestException:
        return []
