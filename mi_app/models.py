from django.db import models


class SolicitudTestVocacional(models.Model):
    nombre = models.CharField(max_length=150)
    edad = models.PositiveIntegerField()
    correo = models.EmailField()
    nivel_educativo = models.CharField(max_length=255)

    # Respuestas
    pregunta1 = models.CharField(max_length=255)
    pregunta2 = models.CharField(max_length=255)
    pregunta3 = models.CharField(max_length=255)
    pregunta4 = models.CharField(max_length=255)
    pregunta5 = models.CharField(max_length=255)

    # Resultado del test
    area_predominante = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    carreras_recomendadas = models.TextField(blank=True)  # guardamos como texto plano (lista unida por comas)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'solicitudes'

    def __str__(self):
        return f"{self.nombre} - {self.area_predominante} ({self.fecha_creacion.date()})"
