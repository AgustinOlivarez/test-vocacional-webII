from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from .forms import TestVocacionalForm
from collections import Counter
from django.core.mail import send_mail
from django.conf import settings
from .models import SolicitudTestVocacional
from .serializers import SolicitudSerializer
from .utils import traducir_texto
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

class SolicitudesView(APIView):
    def get(self, request):
        solicitudes = SolicitudTestVocacional.objects.all().order_by('-id')
        serializer = SolicitudSerializer(solicitudes, many=True)
        return Response(serializer.data)

class TraducirView(APIView):
    def post(self, request):
        texto = request.data.get("texto")
        de_lang = request.data.get("de", "es")
        a_lang = request.data.get("a", "en")

        url = "https://api.mymemory.translated.net/get"
        params = {'q': texto, 'langpair': f'{de_lang}|{a_lang}'}
        response = requests.get(url, params=params)
        data = response.json()

        traduccion = data.get('responseData', {}).get('translatedText', texto)
        return Response({"traduccion": traduccion})

def pagina_inicio(request):
    if request.method == 'POST':
        form = TestVocacionalForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            edad = form.cleaned_data['edad']
            correo = form.cleaned_data['correo']

            # Validación de edad mínima
            if edad < 16:
                return JsonResponse({
                    'error': 'Debés tener al menos 16 años para realizar el test.'
                })

            # Contamos las respuestas más repetidas
            respuestas = [
                form.cleaned_data['pregunta1'],
                form.cleaned_data['pregunta2'],
                form.cleaned_data['pregunta3'],
                form.cleaned_data['pregunta4'],
                form.cleaned_data['pregunta5']
            ]
            area_predominante = Counter(respuestas).most_common(1)[0][0]

            descripciones = {
                "Ciencias Exactas": "Te destacás por tu pensamiento lógico, capacidad de análisis y resolución de problemas.",
                "Ciencias Sociales": "Tenés una fuerte inclinación por entender a las personas y su entorno.",
                "Arte y Creatividad": "Sos una persona expresiva, original y con mucha imaginación.",
                "Tecnología e Informática": "Tenés afinidad por lo técnico, lo digital y lo innovador.",
                "Salud": "Te mueve el cuidado de los demás. Sos empático, solidario y con gran interés por el bienestar físico y emocional."
            }

            descripcion_original = descripciones.get(area_predominante, '')
            descripcion_traducida = traducir_texto(descripcion_original, de='es', a='en')

            carreras = {
                "Ciencias Exactas": ["Lic. en Matemática", "Ingeniería Civil", "Economía", "Física"],
                "Ciencias Sociales": ["Psicología", "Trabajo Social", "Derecho", "Ciencias de la Educación"],
                "Arte y Creatividad": ["Diseño Gráfico", "Bellas Artes", "Artes Dramáticas", "Música"],
                "Tecnología e Informática": ["Ingeniería en Sistemas", "Lic. en Informática",
                                             "Tecnicatura en Programación", "Desarrollo Web"],
                "Salud": ["Medicina", "Enfermería", "Nutrición", "Kinesiología"]
            }
            carreras_recomendadas = carreras.get(area_predominante, [])
            carreras_traducidas = [
                traducir_texto(carrera, de='es', a='en') for carrera in carreras_recomendadas
            ]
            informe = f"""
            Hola {nombre},

            Gracias por completar el Test Vocacional de Vaccari.

            Tu perfil profesional es: {area_predominante}
            Edad: {edad} años

            Próximamente recibirás más información sobre carreras recomendadas.

            Atentamente,
            El equipo de Vaccari
            """
            SolicitudTestVocacional.objects.create(
                nombre=nombre,
                edad=edad,
                correo=correo,
                nivel_educativo=form.cleaned_data['nivel_educativo'],
                pregunta1=form.cleaned_data['pregunta1'],
                pregunta2=form.cleaned_data['pregunta2'],
                pregunta3=form.cleaned_data['pregunta3'],
                pregunta4=form.cleaned_data['pregunta4'],
                pregunta5=form.cleaned_data['pregunta5'],
                area_predominante=area_predominante,
                descripcion=descripcion_original,
                carreras_recomendadas=", ".join(carreras.get(area_predominante, []))
            )
            send_mail(
                subject='Confirmación - Informe Vocacional',
                message=informe,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[correo],
                fail_silently=False,
            )
            return JsonResponse({
                'nombre': nombre,
                'area': area_predominante,
                'descripcion': descripcion_original,
                'descripcion_traducida': descripcion_traducida,
                'carreras': carreras_recomendadas,
                'carreras_traducidas': carreras_traducidas,
            })
        else:
            return JsonResponse({'error': 'Formulario inválido. Verificá los datos.'})

    else:
        form = TestVocacionalForm()
        return render(request, 'mi_app/index.html', {'form': form})

@login_required
def panel_solicitudes(request):
    solicitudes = SolicitudTestVocacional.objects.all().order_by('-id')
    return render(request, 'mi_app/panel_solicitudes.html', {'solicitudes': solicitudes})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('panel_solicitudes')  # si ya está logueado

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('panel_solicitudes')  # 👈 redirección al panel
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()

    return render(request, 'mi_app/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('panel_solicitudes')  # si ya está logueado

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # loguea automáticamente tras registrarse
            return redirect('panel_solicitudes')
    else:
        form = UserCreationForm()

    return render(request, 'mi_app/register.html', {'form': form})


