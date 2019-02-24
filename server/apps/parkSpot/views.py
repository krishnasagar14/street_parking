from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import exceptions, status
from drf_yasg.utils import swagger_auto_schema
from django.db.models import F, Func

from .models import parkingSpot
from .serializers import SpotAvailSerializer, SpotModelSerializer
from common.serializers import GenericRespSerializer
from core.views import AppResponse
from common.parameters import auth
from .parameters import lat, longi, radius
# Create your views here.

spots_model_fiels = [k for k in SpotModelSerializer().fields.keys()]

class ParkingSpotsAvail(AppResponse, GenericAPIView):
    """
    API for free parking spots of street.
    """
    serializer_class = SpotAvailSerializer
    authentication_classes = ()

    @swagger_auto_schema()
    def get(self, request, format=None):
        output = list()
        free_parking_slots = parkingSpot.objects.filter(is_reserved=False).values(*spots_model_fiels)
        if free_parking_slots:
            output = free_parking_slots
        return Response(self.get_data(output), status=status.HTTP_200_OK)

class SearchParkingSpot(AppResponse, GenericAPIView):
    """
    API for searching parking spot using input radius, latitude and longitude
    """
    serializer_class = SpotAvailSerializer

    @swagger_auto_schema(
        manual_parameters=[auth, radius, lat, longi],
        responses={
            400: GenericRespSerializer,
            401: GenericRespSerializer,
        }
    )
    def get(self, request, format=None):
        output = dict()

        try:
            rad = int(request.GET['radius']) ** 2
            latitude = int(request.GET['Latitude'])
            longitude = int(request.GET['Longitude'])
        except Exception as e:
            output['message'] = 'REQUEST_PARAMS_INCOMPLETE'
            return Response(self.get_data(output), status=status.HTTP_400_BAD_REQUEST)

        near_spots = parkingSpot.objects.filter(is_reserved=False).annotate(radius=((F('lat')-latitude) ** 2\
            + (F('longi')-longitude) ** 2)).filter(radius__lt=rad).values(*spots_model_fiels)
        return Response(self.get_data(near_spots), status=status.HTTP_200_OK)