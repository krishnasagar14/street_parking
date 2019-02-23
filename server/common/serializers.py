from rest_framework import serializers

class MesgSerializer(serializers.Serializer):
    message = serializers.CharField(help_text="Message code eg: USER_SUCCESS")

class GenericRespSerializer(serializers.Serializer):
    data = MesgSerializer()