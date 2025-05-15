import os
import requests


def get_faq(question: str) -> dict:
    base_url = f'{os.getenv("BASE_API_URL")}/faqs'
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        faqs = response.json().get("values", [])
    except requests.RequestException as e:
        return f"Error al consultar las preguntas frecuentes: {e}"

    question_lower = question.lower()

    # Palabras clave para identificar preguntas relacionadas con "vinculación"
    vincular_keywords = [
        "vincular",
        "trabajar",
        "ser parte",
        "unirme",
        "participar",
        "ser piragüero",
        "colaborar",
        "hacer parte",
        "cómo ser piragüero",
        "cómo puedo ser",
        "quiero ser piragüero",
        "convertirme en piragüero",
        "ingresar",
        "postularme",
        "formar parte",
        "hacer parte del equipo",
        "reclutamiento",
        "me interesa ser",
        "cómo aplicar",
        "cómo ingreso",
        "cómo hago parte",
        "oferta laboral",
        "oportunidades",
        "voluntario",
        "cómo colaborar",
        "cómo contribuir",
    ]
    # Palabras clave para identificar preguntas sobre "qué es piragua"
    que_es_keywords = ["qué es piragua", "que es piragua", "piragua"]

    # Buscar por coincidencia exacta o inclusión
    for faq in faqs:
        faq_pregunta_lower = faq["pregunta"].lower()
        if faq_pregunta_lower in question_lower or question_lower in faq_pregunta_lower:
            return {"pregunta": faq["pregunta"], "respuesta": faq["respuesta"]}

    # Buscar por palabras clave de vinculación
    if any(word in question_lower for word in vincular_keywords):
        for faq in faqs:
            if "piragüero" in faq["pregunta"].lower():
                return {"pregunta": faq["pregunta"], "respuesta": faq["respuesta"]}

    # # Buscar por palabras clave de "qué es piragua"
    # if any(word in question_lower for word in que_es_keywords):
    #     for faq in faqs:
    #         if "qué es piragua" in faq["pregunta"].lower():
    #             return {"pregunta": faq["pregunta"], "respuesta": faq["respuesta"]}

    return "No se encontró una respuesta para tu pregunta en las preguntas frecuentes."
