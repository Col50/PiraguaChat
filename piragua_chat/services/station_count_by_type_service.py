from piragua_chat.services.common_utility_service import normalize_text
from piragua_chat.services.station_by_municipality_service import (
    get_station_codes_by_municipality,
)
from piragua_chat.services.municipality_service import get_municipalities


TIPO_MAP = {
    "pluviografica": "1",
    "limnigrafica": "2",
    "meteorologica": "8",
    "piezometro": "6",
}


def get_station_count_by_type(municipality_name: str, type_name: str) -> dict:
    """
    Devuelve la cantidad de estaciones de un tipo específico en el municipio dado.
    municipality_id: id del municipio (str)
    tipo_nombre: nombre del tipo de estación (ej: 'pluviográfica', 'limnigráfica', etc)
    """
    # 1. Buscar municipio por nombre (normalizando)
    municipalities = get_municipalities().get("municipality", [])
    municipality_name_normalized = normalize_text(municipality_name)
    municipality = next(
        (
            m
            for m in municipalities
            if normalize_text(m.get("nombre", "")) == municipality_name_normalized
        ),
        None,
    )
    if not municipality:
        return {"error": f"No se encontró el municipio '{municipality_name}'."}
    municipality_id = municipality.get("id")
    print(f"municipio_id: {municipality_id}")
    print(f"municipio: {municipality}")
    if not municipality_id:
        return {"error": "El municipio no tiene un ID válido."}
    normalized_type_name = normalize_text(type_name)
    type_param = None
    for key, value in TIPO_MAP.items():
        if key in normalized_type_name:
            type_param = value
            break
    if not type_param:
        return {"error": "No se reconoció el tipo de estación solicitado."}

    # Usar get_station_codes_by_municipality para obtener los códigos de estación filtrando por tipo
    codes = get_station_codes_by_municipality(municipality_id, type_param)
    print(f"codigos: {codes}")
    return {
        "municipio_id": municipality_id,
        "tipo": type_name,
        "cantidad_estaciones": len(codes),
    }
