from rest_framework import serializers
from .models import SolicitudTestVocacional

class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudTestVocacional
        fields = '__all__'