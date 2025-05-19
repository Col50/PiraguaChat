import os
import requests


def get_station_code_by_source(source_name: str) -> str:
    base_url = f'{os.getenv("BASE_API_URL")}/estaciones'
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        estaciones = response.json().get("values", [])
        for est in estaciones:
            if est.get("fuente", "").lower() == source_name.lower():
                return est.get("codigo")
        return None
    except requests.RequestException:
        return None
