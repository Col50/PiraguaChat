import os
import requests
from piragua_chat.services.municipality_service import get_municipality
from piragua_chat.services.normalize_text_service import normalize_text
from piragua_chat.services.station_by_municipality_service import (
    get_station_codes_by_municipality,
)


def count_thresholds_by_municipality(municipality_name: str, threshold: str) -> dict:
    """
    Cuenta los umbrales (ROJO, NARANJA, AMARILLO) reportados en todos los puntos de monitoreo de un municipio.
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
        return {"error": f"No se encontró el municipio '{municipality_name}'."}
    municipality_id = municipality.get("id")
    if not municipality_id:
        return {"error": "El municipio no tiene un ID válido."}

    # 2. Buscar estaciones del municipio usando el nuevo servicio
    codes = get_station_codes_by_municipality(municipality_id, "1")
    print(f"codigos: {codes}")
    if not codes:
        return {"error": "No se encontraron estaciones para el municipio."}

    # 3. Contar umbrales para cada estación
    print(f"------Consultando eventos de precipitación para las estaciones: {codes}")
    total = 0
    thresholds_url = f'{os.getenv("BASE_API_URL")}/umbrales'
    for code in codes:
        try:
            resp = requests.get(
                thresholds_url, params={"estacion": code, "umbral": threshold.upper()}
            )
            resp.raise_for_status()
            thresholds = resp.json().get("values", [])
            total += len(thresholds)
        except requests.RequestException:
            continue

    return {
        "municipio": municipality.get("nombre"),
        "umbral": threshold.upper(),
        "total": total,
    }
