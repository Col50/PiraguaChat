import unicodedata


def normalize_text(text: str) -> str:
    """
    Normaliza el texto eliminando tildes y convirtiendo a minúsculas.
    """
    if not text:
        return ""
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text.lower()
