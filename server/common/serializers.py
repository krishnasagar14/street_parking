from rest_framework import serializers

class MesgSerializer(serializers.Serializer):
    message = serializers.CharField(help_text="Message code eg: USER_SUCCESS")
    error = serializers.CharField(help_text='detailed error if response is for 4xx, 5xx status codes')

class GenericRespSerializer(serializers.Serializer):
    data = MesgSerializer()