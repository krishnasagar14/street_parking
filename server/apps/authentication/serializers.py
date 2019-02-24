from rest_framework import serializers

from apps.user.models import User

class LoginReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

class LoginRespSerializer(serializers.Serializer):
    token = serializers.CharField(help_text='Authorization token')

class RegisterSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = super(RegisterSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'mobile_no']