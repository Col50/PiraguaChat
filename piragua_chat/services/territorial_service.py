import os
import requests


def get_territories() -> dict:
    base_url = f'{os.getenv("BASE_API_URL")}/territoriales'
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        territorial = response.json().get("values", [])
        return {"territorial": territorial}
    except requests.RequestException as e:
        return f"Error al consultar los territorios"
