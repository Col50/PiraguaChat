import os
import requests
import unicodedata


def normalize_text(text: str) -> str:
    """
    Normaliza el texto eliminando tildes y convirtiendo a minúsculas.
    """
    if not text:
        return ""
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text.lower()


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
