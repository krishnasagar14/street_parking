from rest_framework import serializers

from .models import parkingSpot

class SpotModelSerializer(serializers.ModelSerializer):
    """
    Parking spot model serializer
    """
    class Meta:
        model = parkingSpot
        fields = ['lat', 'longi', 'spot_addr', 'cost_per_hr']

class SpotAvailSerializer(serializers.Serializer):
    """
    Spot available serializer
    """
    data = SpotModelSerializer(many=True)