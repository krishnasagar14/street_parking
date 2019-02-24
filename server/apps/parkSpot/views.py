from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import exceptions, status
from drf_yasg.utils import swagger_auto_schema

from .models import parkingSpot
from .serializers import SpotAvailSerializer, SpotModelSerializer
from core.views import AppResponse
from common.parameters import auth
# Create your views here.

class ParkingSpotsAvail(AppResponse, GenericAPIView):
    """
    API for free parking spots of street.
    """
    serializer_class = SpotAvailSerializer
    authentication_classes = ()

    @swagger_auto_schema()
    def get(self, request, format=None):
        output = list()
        filter_fields = [k for k in SpotModelSerializer().fields.keys()]
        free_parking_slots = parkingSpot.objects.filter(is_reserved=False).values(*filter_fields)
        if free_parking_slots:
            output = free_parking_slots
        return Response(self.get_data(output), status=status.HTTP_200_OK)