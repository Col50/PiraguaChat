import os
import requests
from piragua_chat.services.normalize_text_service import normalize_text


def get_station_code_by_source(source_name: str) -> str:
    """
    Busca el código de estación por nombre de fuente (río/quebrada).
    """
    base_url = f'{os.getenv("BASE_API_URL")}/estaciones'
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        estaciones = response.json().get("values", [])
        for est in estaciones:
            fuente_normalized = normalize_text(est.get("fuente", ""))
            source_name_normalized = normalize_text(source_name)
            if fuente_normalized == source_name_normalized:
                return est.get("codigo")
        return None
    except requests.RequestException:
        return None
