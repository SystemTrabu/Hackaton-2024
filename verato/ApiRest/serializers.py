from rest_framework import serializers


class JSONFileSerializer(serializers.Serializer):
    file = serializers.FileField()