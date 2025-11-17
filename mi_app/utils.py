import requests
from django.conf import settings

def traducir_texto(texto, de='es', a='en'):
    try:
        response = requests.post(
            settings.API_TRADUCTOR_URL,
            json={"texto": texto, "de": de, "a": a}
        )
        if response.status_code == 200:
            return response.json().get("traduccion", texto)
    except Exception:
        pass
    return texto