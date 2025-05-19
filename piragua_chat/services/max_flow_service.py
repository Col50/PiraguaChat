import os
import requests
from piragua_chat.services.station_code_by_source_service import (
    get_station_code_by_source,
)


def get_max_flow_by_source(source_name: str) -> dict:
    codigo = get_station_code_by_source(source_name)
    print(f"codigo------ {codigo}")
    if not codigo:
        return {"error": f"No se encontró estación para la fuente '{source_name}'."}
    base_url = f'{os.getenv("BASE_API_URL")}/estaciones/{codigo}/nivel/diario/'
    try:
        response = requests.get(base_url)
        print(f"response------ {response}")
        response.raise_for_status()
        values = response.json().get("values", [])
        if not values:
            return {"error": "No se encontraron registros de caudal para la estación."}
        # Buscar el registro con mayor caudal
        max_record = max(values, key=lambda x: float(x.get("caudal", "-999.0")))
        return {
            "fecha": max_record.get("fecha"),
            "caudal_maximo": max_record.get("caudal"),
            "codigo_estacion": codigo,
        }
    except requests.RequestException:
        return {"error": "Error al consultar el caudal máximo de la estación."}
