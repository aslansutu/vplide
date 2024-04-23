from rest_framework import serializers


class FileEvaluateSerializer(serializers.Serializer):
    files = serializers.ListField(child=serializers.FileField())

    class Meta:
        fields = ("files",)
