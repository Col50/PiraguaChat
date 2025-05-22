import os
import requests


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
