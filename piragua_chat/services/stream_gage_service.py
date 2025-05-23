import os
import requests
from piragua_chat.services.normalize_text_service import normalize_text
from datetime import datetime, timedelta
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME_PIRAGUA"),
    "user": os.getenv("DB_USER_PIRAGUA"),
    "password": os.getenv("DB_PASSWORD_PIRAGUA"),
    "host": os.getenv("DB_HOST_PIRAGUA"),
    "port": int(os.getenv("DB_PORT")),
}


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
    """
    Consulta el caudal y nivel de una estación de monitoreo.
    """

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
    """
    Busca el evento de caudal máximo registrado en cualquier estación de monitoreo de la fuente dada.
    """
    source_name_normalized = normalize_text(source_name)
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT nd.*
            FROM niveles_diarios nd
            JOIN estaciones e ON nd.estacion_id = e.id
            WHERE translate(lower(e.fuente), 'áéíóúÁÉÍÓÚñÑ', 'aeiouaeiounn') = %s
            ORDER BY nd.caudal DESC
            LIMIT 1;
            """,
            (source_name_normalized,),
        )
        row = cursor.fetchone()
        if row:
            max_flow = [{"fecha": row[1], "caudal": row[3]}]
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


def get_min_flow_by_source(source_name: str) -> dict:
    """
    Busca el evento de caudal mínimo registrado en cualquier estación de monitoreo de la fuente dada.
    """
    source_name_normalized = normalize_text(source_name)
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT nd.*
            FROM niveles_diarios nd
            JOIN estaciones e ON nd.estacion_id = e.id
            WHERE translate(lower(e.fuente), 'áéíóúÁÉÍÓÚñÑ', 'aeiouaeiounn') = %s
            ORDER BY nd.caudal ASC
            LIMIT 1;
            """,
            (source_name_normalized,),
        )
        row = cursor.fetchone()
        if row:
            min_flow = [{"fecha": row[1], "caudal": row[3]}]
        else:
            min_flow = []

        cursor.close()
        connection.close()
        if not min_flow:
            return {"error": "No se encontraron fuentes de monitoreo."}
        return {
            "formaciones": min_flow,
        }
    except Exception as e:
        return {"error": f"Error al consultar la base de datos"}


def get_flow_by_datetime(station_id: int, date_string: str, time: str) -> dict:
    """
    Consulta el caudal registrado en una estación en una fecha y hora específica.
    Parámetros:
        station_id: código de la estación
        date_string: string en formato 'YYYY-MM-DD'
        time: string en formato 'HH' (hora en 24h, ej: '10' para 10am)
    """
    date = datetime.strptime(date_string, "%Y-%m-%d")
    next_date = (date + timedelta(days=1)).strftime("%Y-%m-%d")
    base_url = f'{os.getenv("BASE_API_URL")}/estaciones/{station_id}/nivel/horario/'
    params = {"fecha__gte": date_string, "fecha__lt": next_date}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        values = response.json().get("values", [])
        date_time = f"{date_string}T{time.zfill(2)}:00:00Z"
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
