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
    municipios = get_municipality().get("municipality", [])
    municipality_name_normalized = normalize_text(municipality_name)
    municipio = next(
        (
            m
            for m in municipios
            if normalize_text(m.get("nombre", "")) == municipality_name_normalized
        ),
        None,
    )
    if not municipio:
        return {"error": f"No se encontró el municipio'{municipality_name}'."}
    municipio_id = municipio.get("id")
    if not municipio_id:
        return {"error": "El municipio no tiene un ID válido."}

    # 2. Buscar estaciones meteorológicas del municipio usando el nuevo servicio
    codigos = get_station_codes_by_municipality(municipio_id, "8")
    if not codigos:
        return {
            "error": "No se encontraron estaciones meteorológicas para el municipio."
        }

    # 3. Buscar el evento de precipitación máxima en todas las estaciones
    max_precip = float("-inf")
    max_event = None
    codigo_max = None

    # Llama una sola vez con todos los códigos
    all_records = get_all_meteorological_station_records(codigos)
    for codigo, registros in all_records.items():
        for reg in registros:
            try:
                precip = float(reg.get("lluvia", "-999.0"))
            except (TypeError, ValueError):
                continue
            if precip > max_precip:
                max_precip = precip
                max_event = reg
                codigo_max = codigo

    if max_event:
        return {
            "municipio": municipio.get("nombre"),
            "codigo_estacion": codigo_max,
            "fecha": max_event.get("fecha"),
            "precipitacion_maxima": max_event.get("lluvia"),
        }
    else:
        return {
            "error": "No se encontraron registros de precipitación para las estaciones del municipio."
        }


def get_rain_by_datetime(station_id: int, fecha: str, hora: str) -> dict:
    """
    Consulta el nivel de lluvia registrado en una estación meteorológica en una fecha y hora específica.
    Parámetros:
        station_id: código de la estación
        fecha: string en formato 'YYYY-MM-DD'
        hora: string en formato 'HH' (hora en 24h, ej: '10' para 10am)
    """
    # Calcular fecha siguiente para fecha__lt
    fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
    fecha_siguiente = (fecha_dt + timedelta(days=1)).strftime("%Y-%m-%d")
    base_url = (
        f'{os.getenv("BASE_API_URL")}/estaciones/{station_id}/meteorologia/horario/'
    )
    params = {"fecha__gte": fecha, "fecha__lt": fecha_siguiente}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        values = response.json().get("values", [])
        # Construir el string de fecha completa en formato ISO
        fecha_hora = f"{fecha}T{hora.zfill(2)}:00:00Z"
        for reg in values:
            if reg.get("fecha") == fecha_hora:
                return {
                    "fecha": reg.get("fecha"),
                    "lluvia": reg.get("lluvia"),
                    "id": reg.get("id"),
                }
        return {"error": f"No se encontró registro para la fecha y hora {fecha_hora}."}
    except requests.RequestException:
        return {"error": "Error al consultar los datos de la estación."}
