import requests
from django.conf import settings
import os


def traducir_texto(texto, de='es', a='en'):
    if not texto:
        return texto

    try:
        # Determinar URL según entorno
        base_url = settings.API_TRADUCTOR_URL

        # Si la URL contiene onrender.com, reemplazar con localhost
        if 'onrender.com' in base_url:
            port = os.getenv('PORT', '10000')
            url = f"http://127.0.0.1:{port}/api/traducir/"
        else:
            url = base_url

        response = requests.post(
            url,
            json={"texto": texto, "de": de, "a": a},
            timeout=10
        )

        if response.status_code == 200:
            return response.json().get("traduccion", texto)

    except requests.exceptions.Timeout:
        print("Timeout en traducción")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

    return texto