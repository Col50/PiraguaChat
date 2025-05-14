import os
import requests
from typing import Optional


def get_hydrobiological_report(report_id: Optional[str] = None) -> dict:
    base_url = f'{os.getenv("BASE_API_URL")}/hidrobiologicos'

    if not report_id:
        return "Entrada vacía. Por favor, proporcione el codigo de un reporte."

    report_id = report_id.strip().strip('"').strip("'").upper()
    url = f"{base_url}/{report_id}/reporte"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return {"report_id": report_id, "url": url}
    except requests.RequestException as e:
        raise ValueError(f"No se pudo encontrar el reporte hidrobiológico: {e}")
