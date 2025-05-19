import os
import requests
from piragua_chat.services.station_code_by_source_service import (
    get_station_codes_by_source,
)


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
