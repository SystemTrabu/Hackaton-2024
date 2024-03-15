from rest_framework import serializer
from .models import ussers

class UssersSerializer(serializer.Modelserializer):
    class Meta:
        model=ussers
        fields='__all__'