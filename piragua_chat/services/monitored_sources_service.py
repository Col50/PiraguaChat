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


def get_monitored_sources_by_municipality(municipality_name: str) -> dict:
    """
    Devuelve la lista de fuentes (quebradas/ríos) monitoreadas en el municipio dado.
    """
    municipality_name = normalize_text(municipality_name)
    print(f"municipality_name: {municipality_name}")

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        # Buscar el id del municipio por nombre (ignorando tildes y mayúsculas)
        cur.execute(
            """
            SELECT id FROM municipios
            WHERE translate(lower(nombre), 'áéíóúÁÉÍÓÚñÑ', 'aeiouaeiounn') = %s
            LIMIT 1
            """,
            (municipality_name,),
        )
        row = cur.fetchone()
        if not row:
            return {"error": f"No se encontró el municipio '{municipality_name}'."}
        municipio_id = row[0]
        # Buscar las fuentes asociadas al municipio
        cur.execute(
            """
            SELECT nombre FROM fuentes_hidricas
            WHERE municipio_id = %s
        """,
            (municipio_id,),
        )
        fuentes = [r[0] for r in cur.fetchall()]
        cur.close()
        conn.close()
        if not fuentes:
            return {
                "error": "No se encontraron fuentes monitoreadas para el municipio."
            }
        return {"municipio": municipality_name, "fuentes_monitoreadas": fuentes}
    except Exception as e:
        return {"error": f"Error al consultar la base de datos: {str(e)}"}
