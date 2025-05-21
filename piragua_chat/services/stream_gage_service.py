import os
import requests
from piragua_chat.services.normalize_text_service import normalize_text
from datetime import datetime, timedelta


def get_station_codes_by_source(source_name: str) -> list:
    """
    Busca todos los códigos de estación por nombre de fuente (río/quebrada).
    """
    base_url = f'{os.getenv("BASE_API_URL")}/estaciones'
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        station = response.json().get("values", [])
        source_name_normalized = normalize_text(source_name)
        codes = [
            est.get("codigo")
            for est in station
            if normalize_text(est.get("fuente", "")) == source_name_normalized
        ]
        return codes
    except requests.RequestException:
        return []


def get_stream_gage(station_id: int) -> dict:
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
        # Buscar el registro con la fecha más reciente
        latest = max(values, key=lambda x: x.get("fecha", ""))
        return {
            "fecha": latest.get("fecha"),
            "caudal": latest.get("caudal"),
            "nivel": latest.get("nivel"),
            "id": latest.get("id"),
        }
    except requests.RequestException:
        return {"error": "Error al consultar los datos de nivel de la estación."}


def get_max_flow_by_source(source_name: str) -> dict:
    codes = get_station_codes_by_source(source_name)
    if not codes:
        return {"error": f"No se encontró estación para la fuente '{source_name}'."}
    max_record = None
    max_flow = float("-inf")
    code_max = None
    for code in codes:
        base_url = f'{os.getenv("BASE_API_URL")}/estaciones/{code}/nivel/diario/'
        try:
            response = requests.get(base_url)
            response.raise_for_status()
            values = response.json().get("values", [])
            if not values:
                continue
            record = max(
                values, key=lambda x: float(x.get("caudal", "-999.0"))
            )  # obtiene el registro con el caudal máximo
            flow = float(record.get("caudal", "-999.0"))
            if flow > max_flow:
                max_flow = flow
                max_record = record
                code_max = code
        except requests.RequestException:
            continue
    if max_record:
        return {
            "fecha": max_record.get("fecha"),
            "caudal_maximo": max_record.get("caudal"),
            "codigo_estacion": code_max,
        }
    else:
        return {"error": "No se encontraron registros de caudal para las estaciones."}


def get_min_flow_by_source(source_name: str) -> dict:
    codes = get_station_codes_by_source(source_name)
    if not codes:
        return {"error": f"No se encontró estación para la fuente '{source_name}'."}
    min_record = None
    min_flow = float("-inf")
    code_min = None
    for code in codes:
        base_url = f'{os.getenv("BASE_API_URL")}/estaciones/{code}/nivel/diario/'
        try:
            response = requests.get(base_url)
            response.raise_for_status()
            values = response.json().get("values", [])
            if not values:
                continue
            record = min(
                values, key=lambda x: float(x.get("caudal", "-999.0"))
            )  # obtiene el registro con el caudal máximo
            flow = float(record.get("caudal", "-999.0"))
            if flow > min_flow:
                min_flow = flow
                min_record = record
                code_min = code
        except requests.RequestException:
            continue
    if min_record:
        return {
            "fecha": min_record.get("fecha"),
            "caudal_minimo": min_record.get("caudal"),
            "codigo_estacion": code_min,
        }
    else:
        return {"error": "No se encontraron registros de caudal para las estaciones."}


def get_flow_by_datetime(station_id: int, date: str, hora: str) -> dict:
    """
    Consulta el caudal registrado en una estación en una fecha y hora específica.
    Parámetros:
        station_id: código de la estación
        fecha: string en formato 'YYYY-MM-DD'
        hora: string en formato 'HH' (hora en 24h, ej: '10' para 10am)
    """
    date_dt = datetime.strptime(date, "%Y-%m-%d")
    next_date = (date_dt + timedelta(days=1)).strftime("%Y-%m-%d")
    base_url = f'{os.getenv("BASE_API_URL")}/estaciones/{station_id}/nivel/horario/'
    params = {"fecha__gte": date, "fecha__lt": next_date}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        values = response.json().get("values", [])
        date_time = f"{date}T{hora.zfill(2)}:00:00Z"
        for reg in values:
            if reg.get("fecha") == date_time:
                return {
                    "fecha": reg.get("fecha"),
                    "caudal": reg.get("caudal"),
                    "nivel": reg.get("nivel"),
                    "id": reg.get("id"),
                }
        return {"error": f"No se encontró registro para la fecha y hora {date_time}."}
    except requests.RequestException:
        return {"error": "Error al consultar los datos de la estación."}
