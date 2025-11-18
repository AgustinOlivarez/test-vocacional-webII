import requests

def traducir_texto(texto, de='es', a='en'):
    if not texto:
        return texto

    try:
        url = "https://api.mymemory.translated.net/get"
        params = {
            'q': texto,
            'langpair': f'{de}|{a}'
        }

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return data.get('responseData', {}).get('translatedText', texto)

    except requests.exceptions.Timeout:
        print("Timeout en traducción")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

    return texto
