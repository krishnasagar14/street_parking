from rest_framework import serializers

class ReserveSpotSerializer(serializers.Serializer):
    spot_id = serializers.CharField(help_text='spot id issued by service')
    duration = serializers.IntegerField(help_text='Duration for reservation in integer hours')

class ReserveSpotSerializer(serializers.Serializer):
    duration = serializers.IntegerField(help_text='Duration for each spot booked')
    spot_id = serializers.CharField(help_text='Spot ID booked')
    spot_cost_per_hr = serializers.IntegerField(help_text='Booked spot cost per hour')

class ReservationsSerializer(serializers.Serializer):
    total_cost = serializers.IntegerField(help_text='Total cost of reservations occupied by user')
    reservations = ReserveSpotSerializer(many=True)

class ReservationsViewSerializer(serializers.Serializer):
    data = ReservationsSerializer()