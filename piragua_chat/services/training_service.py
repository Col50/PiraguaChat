import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME_PIRAGUA"),
    "user": os.getenv("DB_USER_PIRAGUA"),
    "password": os.getenv("DB_PASSWORD_PIRAGUA"),
    "host": os.getenv("DB_HOST_PIRAGUA"),
    "port": int(os.getenv("DB_PORT")),
}


def get_training_name() -> dict:
    """
    Devuelve la cantidad de fuentes (quebradas/ríos) monitoreadas en el municipio dado.
    """
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT nombre FROM nombres_asistencias
            """
        )
        trainings_name = [row[0] for row in cursor.fetchall()]
        cursor.close()
        connection.close()
        if not trainings_name:
            return {"error": "No se pueden obtener la lista de formaciones."}
        return {
            "formaciones": trainings_name,
        }
    except Exception as e:
        return {"error": f"Error al consultar la base de datos"}
