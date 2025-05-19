import os
import requests


def get_municipality() -> dict:
    base_url = f'{os.getenv("BASE_API_URL")}/municipios'
    params = {"simple": "simple"}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        municipality = response.json().get("values", [])
        return {"municipality": municipality}
    except requests.RequestException as e:
        return f"Error al consultar los municipios"
