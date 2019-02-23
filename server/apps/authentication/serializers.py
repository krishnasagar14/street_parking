from rest_framework import serializers

from apps.user.models import User

class LoginReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

class LoginRespSerializer(serializers.Serializer):
    token = serializers.CharField(help_text='Authorization token')