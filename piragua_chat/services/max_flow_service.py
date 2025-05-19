import os
import requests
from piragua_chat.services.station_code_by_source_service import (
    get_station_codes_by_source,
)


def get_max_flow_by_source(source_name: str) -> dict:
    codigos = get_station_codes_by_source(source_name)
    print(f"codigos------ {codigos}")
    if not codigos:
        return {"error": f"No se encontró estación para la fuente '{source_name}'."}
    max_record = None
    max_caudal = float("-inf")
    codigo_max = None
    for codigo in codigos:
        base_url = f'{os.getenv("BASE_API_URL")}/estaciones/{codigo}/nivel/diario/'
        try:
            response = requests.get(base_url)
            print(f"response------ {response}")
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
