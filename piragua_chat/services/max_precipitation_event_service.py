import os
import requests
from piragua_chat.services.municipality_service import get_municipality
from piragua_chat.services.normalize_text_service import normalize_text
from piragua_chat.services.station_by_municipality_service import (
    get_station_codes_by_municipality,
)
from piragua_chat.services.weather_station_service import (
    get_all_weather_station_records,
)


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
    codigos = get_station_codes_by_municipality(municipio_id)
    if not codigos:
        return {
            "error": "No se encontraron estaciones meteorológicas para el municipio."
        }

    # 3. Buscar el evento de precipitación máxima en todas las estaciones
    max_precip = float("-inf")
    max_event = None
    codigo_max = None

    # Llama una sola vez con todos los códigos
    all_records = get_all_weather_station_records(codigos)
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
