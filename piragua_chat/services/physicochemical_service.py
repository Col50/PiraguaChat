import os
from traceback import print_tb
import requests
from piragua_chat.services.normalize_text_service import normalize_text


def get_physicochemical_report(report_id: str) -> dict:
    base_url = f'{os.getenv("BASE_API_URL")}/fisicoquimicos'

    if not report_id.strip():
        return "Entrada vacía. Por favor, proporcione el ID de un reporte."

    report_id = report_id.strip().strip('"').strip("'").upper()
    url = f"{base_url}/{report_id}/reporte"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return {"report_id": report_id, "url": url}
    except requests.RequestException as e:
        return f"No se pudo encontrar el reporte físico-químico:"


def get_station_code_by_water_monitoring_name(source_name: str) -> list:
    """
    Busca todos los códigos de estaciones de monitoreo aguas subterraneas por nombre.
    """
    print(f"Buscando códigos de estaciones para la fuente: {source_name}")
    base_url = f'{os.getenv("BASE_API_URL")}/fisicoquimicos'
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        estaciones = response.json().get("values", [])
        source_name_normalized = normalize_text(source_name)
        codes = [
            est.get("codigo")
            for est in estaciones
            if normalize_text(est.get("fuente", "")) == source_name_normalized
        ]
        return codes
    except requests.RequestException:
        return []


def get_water_quality(source_name: str) -> dict:
    codigos = get_station_code_by_water_monitoring_name(source_name)
    print(f"Codigos encontrados: {codigos}")
    return {"codigos": codigos}


def get_last_water_quality_measurement(source_name: str) -> dict:
    """
    Consulta la última medición de calidad en los puntos de monitoreo (por nombre de fuente) y resume todos los parámetros disponibles.
    Si hay varias estaciones, toma la medición más reciente entre todas.
    """
    stations_code = get_station_code_by_water_monitoring_name(source_name)
    print(f"stations_code {stations_code}")

    if not stations_code:
        return {"error": "No se encontraron estaciones para la fuente indicada."}

    latest = None
    latest_station = None

    for station_code in stations_code:
        base_url = f'{os.getenv("BASE_API_URL")}/fisicoquimicos/{station_code}/resultados'
        print(f"base_url ----- {base_url}")
        try:
            response = requests.get(base_url)
            response.raise_for_status()
            items = response.json().get("items", [])
            if not items:
                continue
            station_latest = max(items, key=lambda x: x.get("fecha", ""))
            if (latest is None) or (station_latest.get("fecha", "") > latest.get("fecha", "")):
                latest = station_latest
                latest_station = station_code
        except requests.RequestException:
            continue

    if not latest:
        return {"error": "No se encontraron mediciones para los puntos de monitoreo."}

    parametros = latest.get("parametros", {})
    resumen = {nombre: info.get("muestra") for nombre, info in parametros.items()}
    return {
        "codigo_estacion": latest_station,
        "fecha": latest.get("fecha"),
        "calidad": latest.get("calidad"),
        "ica": latest.get("ica"),
        "resumen_parametros": resumen,
    }
