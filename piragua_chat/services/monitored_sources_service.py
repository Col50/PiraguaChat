import psycopg2
import os
from dotenv import load_dotenv
from piragua_chat.services.normalize_text_service import normalize_text

load_dotenv()
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME_PIRAGUA"),
    "user": os.getenv("DB_USER_PIRAGUA"),
    "password": os.getenv("DB_PASSWORD_PIRAGUA"),
    "host": os.getenv("DB_HOST_PIRAGUA"),
    "port": int(os.getenv("DB_PORT")),
}


def get_municipality_id_by_name(municipality_name: str):
    """
    Devuelve el id del municipio dado su nombre normalizado.
    Retorna None si no se encuentra.
    """
    municipality_name = normalize_text(municipality_name)
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id FROM municipios
                    WHERE translate(lower(nombre), 'áéíóúÁÉÍÓÚñÑ', 'aeiouaeiounn') = %s
                    LIMIT 1
                    """,
                    (municipality_name,),
                )
                row = cur.fetchone()
                if row:
                    return row[0]
    except Exception as e:
        print(f"Error al obtener el id del municipio")
    return None


def get_monitored_sources(municipality_name: str) -> dict:
    """
    Devuelve la lista de fuentes (quebradas/ríos) monitoreadas en el municipio dado.
    """
    municipality_id = get_municipality_id_by_name(municipality_name)
    if not municipality_id:
        return {"error": f"No se encontró el municipio '{municipality_name}'."}
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT nombre FROM fuentes_hidricas
            WHERE municipio_id = %s
            """,
            (municipality_id,),
        )
        sources = [r[0] for r in cur.fetchall()]
        cur.close()
        conn.close()
        if not sources:
            return {
                "error": "No se encontraron fuentes monitoreadas para el municipio."
            }
        print(f"fuentes------:{sources}")
        return {"municipio": municipality_name, "fuentes_monitoreadas": sources}
    except Exception as e:
        return {"error": f"Error al consultar la base de datos"}


def get_monitoring_points_location(municipality_name: str) -> dict:
    """
    Devuelve la ubicación (altitud, longitud, latitud) de los puntos de monitoreo en el municipio dado.
    """
    municipality_name = normalize_text(municipality_name)
    print(f"ENTRA A get_monitoring_points_location")

    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT nombre, altitud, longitud, latitud FROM fuentes_hidricas 
                    WHERE translate(lower(nombre), 'áéíóúÁÉÍÓÚñÑ', 'aeiouaeiounn') = %s
                    """,
                    (municipality_name,),
                )
                resultados = cur.fetchall()
                print("Resultados obtenidos de la base de datos:")
                for r in resultados:
                    print(r)

                puntos = [
                    {
                        "nombre": r[0],
                        "altitud": r[1],
                        "longitud": r[2],
                        "latitud": r[3],
                    }
                    for r in resultados
                ]

        if not puntos:
            return {"error": "No se encontraron puntos de monitoreo para el municipio."}
        return {"municipio": municipality_name, "puntos_monitoreo": puntos}
    except Exception as e:
        return {"error": f"Error al consultar la base de datos"}


def get_count_monitored_sources(municipality_name: str) -> dict:
    """
    Devuelve la cantidad de fuentes (quebradas/ríos) monitoreadas en el municipio dado.
    """
    municipality_id = get_municipality_id_by_name(municipality_name)
    print(f"municipio_id: {municipality_id}")
    if not municipality_id:
        return {"error": f"No se encontró el municipio '{municipality_name}'."}
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT COUNT(*) FROM fuentes_hidricas
            WHERE municipio_id = %s
            """,
            (municipality_id,),
        )
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        if not count:
            return {
                "error": "No se encontraron fuentes monitoreadas para el municipio."
            }
        print(f"count------:{count}")
        return {"municipio": municipality_name, "cantidad_fuentes_monitoreadas": count}
    except Exception as e:
        return {"error": f"Error al consultar la base de datos"}
