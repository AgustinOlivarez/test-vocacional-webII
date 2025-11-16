from django import forms

AREAS = [
    ('Ciencias Exactas', 'Ciencias Exactas'),
    ('Ciencias Sociales', 'Ciencias Sociales'),
    ('Arte y Creatividad', 'Arte y Creatividad'),
    ('Tecnología e Informática', 'Tecnología e Informática'),
    ('Salud', 'Salud'),
]

class TestVocacionalForm(forms.Form):
    nombre = forms.CharField(label="Nombre y Apellido", max_length=100)
    edad = forms.IntegerField(label="Edad", min_value=0)
    correo = forms.EmailField(label="Correo electrónico")

    nivel_educativo = forms.ChoiceField(
        label="Nivel educativo alcanzado",
        choices=[
            ('', 'Seleccioná una opción'),
            ('Primario completo', 'Primario completo'),
            ('Secundario incompleto', 'Secundario incompleto'),
            ('Secundario completo', 'Secundario completo'),
            ('Terciario o universitario en curso', 'Terciario o universitario en curso'),
            ('Terciario o universitario completo', 'Terciario o universitario completo'),
        ]
    )

    pregunta1 = forms.ChoiceField(
        label="¿Qué actividad disfrutas más?",
        choices=[
            ('', 'Seleccioná una opción'),
            ('Ciencias Exactas', 'Resolver problemas matemáticos o de lógica'),
            ('Salud', 'Ayudar a las personas a mejorar su salud'),
            ('Arte y Creatividad', 'Dibujar, pintar o crear cosas nuevas'),
            ('Ciencias Sociales', 'Analizar el comportamiento humano y social'),
            ('Tecnología e Informática', 'Programar, usar computadoras o tecnología'),
        ]
    )

    pregunta2 = forms.ChoiceField(
        label="¿Qué tipo de proyectos te llaman más la atención?",
        choices=[
            ('', 'Seleccioná una opción'),
            ('Ciencias Sociales', 'Organización de campañas solidarias o sociales'),
            ('Ciencias Exactas', 'Investigaciones científicas y experimentos'),
            ('Tecnología e Informática', 'Desarrollo de aplicaciones o videojuegos'),
            ('Salud', 'Charlas de prevención de enfermedades'),
            ('Arte y Creatividad', 'Montajes teatrales o diseño gráfico'),
        ]
    )

    pregunta3 = forms.ChoiceField(
        label="¿Con qué frase te identificas más?",
        choices=[
            ('', 'Seleccioná una opción'),
            ('Arte y Creatividad', 'Me encanta expresarme de manera artística'),
            ('Ciencias Sociales', 'Me interesa entender cómo piensan las personas'),
            ('Tecnología e Informática', 'Siempre quiero estar al día con lo último en tecnología'),
            ('Salud', 'Me preocupa el bienestar físico de las personas'),
            ('Ciencias Exactas', 'Me gusta resolver acertijos y desafíos lógicos'),
        ]
    )

    pregunta4 = forms.ChoiceField(
        label="¿Qué lugar de trabajo te resulta más atractivo?",
        choices=[
            ('', 'Seleccioná una opción'),
            ('Salud', 'Un hospital o centro de salud'),
            ('Ciencias Exactas', 'Un laboratorio con equipos de investigación'),
            ('Arte y Creatividad', 'Un estudio de diseño o escenario de teatro'),
            ('Ciencias Sociales', 'Una ONG o institución educativa'),
            ('Tecnología e Informática', 'Una empresa de software o startup'),
        ]
    )

    pregunta5 = forms.ChoiceField(
        label="¿Qué habilidad consideras que tienes más desarrollada?",
        choices=[
            ('', 'Seleccioná una opción'),
            ('Ciencias Sociales', 'Comunicación y empatía'),
            ('Tecnología e Informática', 'Pensamiento analítico y técnico'),
            ('Arte y Creatividad', 'Creatividad e innovación artística'),
            ('Salud', 'Cuidado y servicio hacia los demás'),
            ('Ciencias Exactas', 'Razonamiento lógico y matemático'),
        ]
    )
