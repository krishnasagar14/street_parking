from rest_framework import serializers

class ReserveSpotSerializer(serializers.Serializer):
    spot_id = serializers.CharField(help_text='spot id issued by service')
    duration = serializers.IntegerField(help_text='Duration for reservation in integer hours')

class ReserveSpotsSerializer(serializers.Serializer):
    reserve_id = serializers.CharField(help_text='Reservation id')
    duration = serializers.IntegerField(help_text='Duration for each spot booked')
    spot_id = serializers.CharField(help_text='Spot ID booked')
    spot_cost_per_hr = serializers.IntegerField(help_text='Booked spot cost per hour')
    cost_per_spot = serializers.IntegerField(help_text='Cost value for per booked spot')

class ReservationsSerializer(serializers.Serializer):
    total_cost = serializers.IntegerField(help_text='Total cost of reservations occupied by user')
    reservations = ReserveSpotsSerializer(many=True)

class ReservationsViewSerializer(serializers.Serializer):
    data = ReservationsSerializer()