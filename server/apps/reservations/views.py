from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import exceptions, status
from drf_yasg.utils import swagger_auto_schema

from core.views import AppResponse
from common.serializers import GenericRespSerializer
from common.parameters import auth
from .serializers import ReserveSpotSerializer
from apps.parkSpot.models import parkingSpot
from .models import Reservations

# Create your views here.

class StreetSpotReservation(AppResponse, GenericAPIView):
    """
    API for street spot reservation for user.
    """
    serializer_class = ReserveSpotSerializer

    @swagger_auto_schema(
        manual_parameters=[auth],
        responses={
            200: GenericRespSerializer,
            400: GenericRespSerializer,
        }
    )
    def post(self, request, format=None):
        output = dict()

        def _response_400(msg='NO_SPOT_FOUND'):
            output['message'] = msg
            return Response(self.get_data(output), status=status.HTTP_400_BAD_REQUEST)

        try:
            spot_id = request.data['spot_id']
        except Exception as e:
            return _response_400()
        try:
            time_period = request.data['duration']
        except Exception as e:
            return _response_400('NO_DURATION_FOUND')
        if time_period <= 0:
            return  _response_400('POSITIVE_DURATION_EXPECTED')

        user_obj = request.user
        spot_obj = None
        try:
            spot_obj = parkingSpot.objects.filter(pk=spot_id).first()
        except Exception as e:
            return _response_400()
        if not spot_obj:
            return _response_400()
        if spot_obj.is_reserved:
            return _response_400('SPOT_IS_ALREADY_RESERVED')

        Reservations.objects.create(user=user_obj, spot=spot_obj, duration=time_period)
        spot_obj.is_reserved = True
        spot_obj.save()

        output['message'] = 'SPOT_RESERVED'
        return Response(self.get_data(output), status=status.HTTP_200_OK)
