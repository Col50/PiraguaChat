import os
import requests
from piragua_chat.services.station_code_by_source_service import (
    get_station_codes_by_source,
)


def get_limnigrafica(station_id: int) -> dict:
    # codigos = get_station_codes_by_source(source_name)
    # if not codigos:
    #     return {"error": f"No se encontró estación para la fuente '{source_name}'."}

    base_url = f'{os.getenv("BASE_API_URL")}/estaciones/{station_id}/nivel'
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        values = response.json().get("values", [])
        if not values:
            return {"error": "No se encontraron registros para la estación."}
        latest = values[0]
        return {
            "fecha": latest.get("fecha"),
            "caudal": latest.get("caudal"),
            "nivel": latest.get("nivel"),
            "id": latest.get("id"),
        }
    except requests.RequestException:
        return {"error": "Error al consultar los datos de nivel de la estación."}


def get_max_flow_by_source(source_name: str) -> dict:
    codigos = get_station_codes_by_source(source_name)
    if not codigos:
        return {"error": f"No se encontró estación para la fuente '{source_name}'."}
    max_record = None
    max_caudal = float("-inf")
    codigo_max = None
    for codigo in codigos:
        base_url = f'{os.getenv("BASE_API_URL")}/estaciones/{codigo}/nivel/diario/'
        try:
            response = requests.get(base_url)
            response.raise_for_status()
            values = response.json().get("values", [])
            if not values:
                continue
            record = max(
                values, key=lambda x: float(x.get("caudal", "-999.0"))
            )  # obtiene el registro con el caudal máximo
            caudal = float(record.get("caudal", "-999.0"))
            if caudal > max_caudal:
                max_caudal = caudal
                max_record = record
                codigo_max = codigo
        except requests.RequestException:
            continue
    if max_record:
        return {
            "fecha": max_record.get("fecha"),
            "caudal_maximo": max_record.get("caudal"),
            "codigo_estacion": codigo_max,
        }
    else:
        return {"error": "No se encontraron registros de caudal para las estaciones."}


def get_min_flow_by_source(source_name: str) -> dict:
    codigos = get_station_codes_by_source(source_name)
    print(f"codigos minimo------ {codigos}")
    if not codigos:
        return {"error": f"No se encontró estación para la fuente '{source_name}'."}
    min_record = None
    min_caudal = float("-inf")
    codigo_min = None
    for codigo in codigos:
        base_url = f'{os.getenv("BASE_API_URL")}/estaciones/{codigo}/nivel/diario/'
        try:
            response = requests.get(base_url)
            print(f"response------ {response}")
            response.raise_for_status()
            values = response.json().get("values", [])
            if not values:
                continue
            record = min(
                values, key=lambda x: float(x.get("caudal", "-999.0"))
            )  # obtiene el registro con el caudal máximo
            caudal = float(record.get("caudal", "-999.0"))
            if caudal > min_caudal:
                min_caudal = caudal
                min_record = record
                codigo_min = codigo
        except requests.RequestException:
            continue
    if min_record:
        return {
            "fecha": min_record.get("fecha"),
            "caudal_minimo": min_record.get("caudal"),
            "codigo_estacion": codigo_min,
        }
    else:
        return {"error": "No se encontraron registros de caudal para las estaciones."}
