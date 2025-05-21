import psycopg2
import os
from dotenv import load_dotenv
from piragua_chat.services.normalize_text_service import normalize_text
from piragua_chat.services.monitored_sources_service import get_municipality_id_by_name

load_dotenv()
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME_PIRAGUA"),
    "user": os.getenv("DB_USER_PIRAGUA"),
    "password": os.getenv("DB_PASSWORD_PIRAGUA"),
    "host": os.getenv("DB_HOST_PIRAGUA"),
    "port": int(os.getenv("DB_PORT")),
}


def get_activities_by_municipality(municipality_name: str) -> dict:
    """
    Devuelve las actividades realizadas en el municipio dado, consultando los grupos piragueros y sus asistencias.
    """
    municipality_id = get_municipality_id_by_name(municipality_name)
    if not municipality_id:
        return {"error": f"No se encontró el municipio '{municipality_name}'."}
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                # Buscar los grupos piragueros del municipio
                cur.execute(
                    """
                    SELECT id FROM grupos_piragueros
                    WHERE municipio_id = %s
                    """,
                    (municipality_id,),
                )
                groups = [r[0] for r in cur.fetchall()]
                if not groups:
                    return {
                        "error": "No se encontraron grupos piragueros para el municipio."
                    }

                # Buscar asistencias para esos grupos
                cur.execute(
                    """
                    SELECT grupo_piraguero_id, fecha_asistencia, nombre_id
                    FROM "Asistencias"
                    WHERE grupo_piraguero_id = ANY(%s::int[])
                    """,
                    (groups,),
                )
                assists = cur.fetchall()
                if not assists:
                    return {
                        "error": "No se encontraron actividades registradas para los grupos piragueros del municipio."
                    }

                # Obtener los nombres de las actividades
                name_ids = list(set([a[2] for a in assists if a[2] is not None]))
                names_activities = {}
                if name_ids:
                    cur.execute(
                        """
                        SELECT id, nombre FROM nombres_asistencias
                        WHERE id = ANY(%s)
                        """,
                        (name_ids,),
                    )
                    names_activities = {r[0]: r[1] for r in cur.fetchall()}

                activities = [
                    {
                        "grupo_piraguero_id": a[0],
                        "fecha_asistencia": a[1],
                        "actividad": names_activities.get(a[2], "Desconocida"),
                    }
                    for a in assists
                ]

        return {
            "municipio_id": municipality_id,
            "municipio": municipality_name,
            "actividades": activities,
        }
    except Exception as e:
        return {"error": f"Error al consultar la base de datos"}
