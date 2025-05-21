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
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT nombre FROM nombres_asistencias
            """
        )
        trainings_name = [r[0] for r in cur.fetchall()]
        cur.close()
        conn.close()
        if not trainings_name:
            return {"error": "No se pueden obtener la lista de formaciones."}
        return {
            "formaciones": trainings_name,
        }
    except Exception as e:
        return {"error": f"Error al consultar la base de datos"}
