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
        return {"error": f"No se encontró el municipio '{municipality_name}'."}
    municipio_id = municipio.get("id")
    if not municipio_id:
        return {"error": "El municipio no tiene un ID válido."}

    # 2. Buscar estaciones del municipio usando el nuevo servicio
    codigos = get_station_codes_by_municipality(municipio_id, "1")
    print(f"codigos: {codigos}")
    if not codigos:
        return {"error": "No se encontraron estaciones para el municipio."}

    # 3. Contar umbrales para cada estación
    print(f"------Consultando eventos de precipitación para las estaciones: {codigos}")
    total = 0
    umbrales_url = f'{os.getenv("BASE_API_URL")}/umbrales'
    for codigo in codigos:
        try:
            resp = requests.get(
                umbrales_url, params={"estacion": codigo, "umbral": threshold.upper()}
            )
            resp.raise_for_status()
            umbrales = resp.json().get("values", [])
            total += len(umbrales)
        except requests.RequestException:
            continue

    return {
        "municipio": municipio.get("nombre"),
        "umbral": threshold.upper(),
        "total": total,
    }
