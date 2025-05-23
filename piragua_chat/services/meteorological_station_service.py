import os
import requests
from piragua_chat.services.municipality_service import get_municipality
from piragua_chat.services.normalize_text_service import normalize_text
import psycopg2
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME_PIRAGUA"),
    "user": os.getenv("DB_USER_PIRAGUA"),
    "password": os.getenv("DB_PASSWORD_PIRAGUA"),
    "host": os.getenv("DB_HOST_PIRAGUA"),
    "port": int(os.getenv("DB_PORT")),
}


def get_meteorological_station(station_id: int) -> dict:
    """
    Retorna el último registro de lluvia de una estación meteorológica.
    """
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
    municipality_name_normalized = normalize_text(municipality_name)
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT md.*
            FROM meteorologias_diarios md
            JOIN estaciones e ON md.estacion_id = e.id
            JOIN municipios m ON e.municipio_id = m.id
            WHERE translate(lower(m.nombre), 'áéíóúÁÉÍÓÚñÑ', 'aeiouaeiounn') = %s
            ORDER BY md.lluvia DESC
            LIMIT 1;
            """,
            (municipality_name_normalized,),
        )
        row = cursor.fetchone()
        if row:
            max_flow = [{"fecha": row[1], "lluvia": row[12]}]
        else:
            max_flow = []

        cursor.close()
        connection.close()
        if not max_flow:
            return {"error": "No se encontraron fuentes de monitoreo."}
        return {
            "formaciones": max_flow,
        }
    except Exception as e:
        return {"error": f"Error al consultar la base de datos"}


def get_rain_by_datetime(station_id: int, date_string: str, time: str) -> dict:
    """
    Consulta el nivel de lluvia registrado en una estación meteorológica en una fecha y hora específica.
    Parámetros:
        station_id: código de la estación
        date_string: string en formato 'YYYY-MM-DD'
        time: string en formato 'HH' (hora en 24h, ej: '10' para 10am)
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
        date_time = f"{date_string}T{time.zfill(2)}:00:00Z"
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
