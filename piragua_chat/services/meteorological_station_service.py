import os
import requests
from piragua_chat.services.municipality_service import get_municipality
from piragua_chat.services.normalize_text_service import normalize_text
from piragua_chat.services.station_by_municipality_service import (
    get_station_codes_by_municipality,
)
from datetime import datetime, timedelta


def get_meteorological_station(station_id: int) -> dict:
    base_url = f'{os.getenv("BASE_API_URL")}/estaciones/{station_id}/meteorologia'
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        values = response.json().get("values", [])
        if not values:
            return {"error": "No se encontraron registros para la estación."}
        latest = values[0]
        return {
            "fecha": latest.get("fecha"),
            "lluvia": latest.get("lluvia"),
            "id": latest.get("id"),
        }
    except requests.RequestException:
        return {"error": "Error al consultar los datos de la estación."}


def get_all_meteorological_station_records(station_ids) -> dict:
    """
    Retorna todos los registros meteorológicos de una o varias estaciones.
    Si una estación falla, continúa con las demás.
    Retorna un diccionario {station_id: [registros]}.
    """
    if not isinstance(station_ids, list):
        station_ids = [station_ids]
    results = {}
    for station_id in station_ids:
        print(f"------Consultando la estación meteorológica: {station_id}")
        base_url = (
            f'{os.getenv("BASE_API_URL")}/estaciones/{station_id}/meteorologia/horario'
        )
        try:
            response = requests.get(base_url)
            response.raise_for_status()
            values = response.json().get("values", [])
            results[station_id] = values
        except requests.RequestException:
            results[station_id] = []
    return results


def get_max_precipitation_event_by_municipality(municipality_name: str) -> dict:
    """
    Busca el evento de precipitación más fuerte registrado en cualquier estación meteorológica del municipio.
    """
    # 1. Buscar municipio por nombre (normalizando)
    municipalitys = get_municipality().get("municipality", [])
    municipality_name_normalized = normalize_text(municipality_name)
    municipality = next(
        (
            m
            for m in municipalitys
            if normalize_text(m.get("nombre", "")) == municipality_name_normalized
        ),
        None,
    )
    if not municipality:
        return {"error": f"No se encontró el municipio'{municipality_name}'."}
    municipality_id = municipality.get("id")
    if not municipality_id:
        return {"error": "El municipio no tiene un ID válido."}

    # 2. Buscar estaciones meteorológicas del municipio usando el nuevo servicio
    codes = get_station_codes_by_municipality(municipality_id, "8")
    if not codes:
        return {
            "error": "No se encontraron estaciones meteorológicas para el municipio."
        }

    # 3. Buscar el evento de precipitación máxima en todas las estaciones
    max_precipitation = float("-inf")
    max_event = None
    code_max = None

    # Llama una sola vez con todos los códigos
    all_records = get_all_meteorological_station_records(codes)
    for code, registers in all_records.items():
        for register in registers:
            try:
                precipitation = float(register.get("lluvia", "-999.0"))
            except (TypeError, ValueError):
                continue
            if precipitation > max_precipitation:
                max_precipitation = precipitation
                max_event = register
                code_max = code

    if max_event:
        return {
            "municipio": municipality.get("nombre"),
            "codigo_estacion": code_max,
            "fecha": max_event.get("fecha"),
            "precipitacion_maxima": max_event.get("lluvia"),
        }
    else:
        return {
            "error": "No se encontraron registros de precipitación para las estaciones del municipio."
        }


def get_rain_by_datetime(station_id: int, date_string: str, hora: str) -> dict:
    """
    Consulta el nivel de lluvia registrado en una estación meteorológica en una fecha y hora específica.
    Parámetros:
        station_id: código de la estación
        fecha: string en formato 'YYYY-MM-DD'
        hora: string en formato 'HH' (hora en 24h, ej: '10' para 10am)
    """
    # Calcular fecha siguiente para fecha__lt
    date = datetime.strptime(date_string, "%Y-%m-%d")
    next_date = (date + timedelta(days=1)).strftime("%Y-%m-%d")
    base_url = (
        f'{os.getenv("BASE_API_URL")}/estaciones/{station_id}/meteorologia/horario/'
    )
    params = {"fecha__gte": date_string, "fecha__lt": next_date}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        values = response.json().get("values", [])
        # Construir el string de fecha completa en formato ISO
        date_time = f"{date_string}T{hora.zfill(2)}:00:00Z"
        for reg in values:
            if reg.get("fecha") == date_time:
                return {
                    "fecha": reg.get("fecha"),
                    "lluvia": reg.get("lluvia"),
                    "id": reg.get("id"),
                }
        return {"error": f"No se encontró registro para la fecha y hora {date_time}."}
    except requests.RequestException:
        return {"error": "Error al consultar los datos de la estación."}
