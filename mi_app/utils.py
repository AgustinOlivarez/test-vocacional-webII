import requests

def traducir_texto(texto, de='es', a='en'):
    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/traducir/",
            json={"texto": texto, "de": de, "a": a}
        )
        if response.status_code == 200:
            return response.json().get("traduccion", texto)
    except Exception:
        pass
    return texto