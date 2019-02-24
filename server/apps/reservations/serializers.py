from rest_framework import serializers

class ReserveSpotSerializer(serializers.Serializer):
    spot_id = serializers.CharField(help_text='spot id issued by service')
    duration = serializers.IntegerField(help_text='Duration for reservation in integer hours')