import math
import datetime
import pytz

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import exceptions, status
from drf_yasg.utils import swagger_auto_schema

from core.views import AppResponse
from common.serializers import GenericRespSerializer
from common.parameters import auth
from .serializers import ReserveSpotSerializer, ReservationsViewSerializer
from apps.parkSpot.models import parkingSpot
from .models import Reservations
from .parameters import reserve_id


def calculate_reservation_spot_cost(resv_obj):
    """
    Helper to calculate cost of reserved spot.
    It will calculate time of reservation from current time - reservation creation time in hours
    then, cost = time of reservation * cost of spot per hour
    :param resv_obj: Reservations model obj containing reservation details
    :return: cost amount rounded off to next integer and reserved time in hours rounded to next integer
    """
    time_diff = datetime.datetime.now(tz=pytz.UTC) - resv_obj.created_at
    time_diff_hrs = math.ceil(time_diff.total_seconds() / (60 * 60))
    cost = time_diff_hrs * resv_obj.spot.cost_per_hr
    return (cost, time_diff_hrs)

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
            time_period = int(request.data['duration'])
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

        resv_obj = Reservations.objects.create(user=user_obj, spot=spot_obj, duration=time_period)
        spot_obj.is_reserved = True
        spot_obj.save()

        output['message'] = 'SPOT_RESERVED'
        output['reserve_id'] = resv_obj.id
        return Response(self.get_data(output), status=status.HTTP_200_OK)

class ViewReservations(AppResponse, GenericAPIView):
    """
    Reservations view API for user with individual costs and total cost.
    """
    serializer_class = ReservationsViewSerializer

    @swagger_auto_schema(
        manual_parameters=[auth],
    )
    def get(self, request, format=None):
        output = dict()
        user_obj = request.user
        resv_obj = Reservations.objects.select_related('spot').filter(user=user_obj)
        total_cost = 0
        res = list()
        for r_obj in resv_obj:
            result = dict()
            result['reserve_id'] = r_obj.id
            cost, time_diff_hrs = calculate_reservation_spot_cost(r_obj)
            result['duration'] = time_diff_hrs
            result['spot_id'] = r_obj.spot.id
            result['spot_cost_per_hr'] = r_obj.spot.cost_per_hr
            result['cost_per_spot'] = cost
            total_cost += result['cost_per_spot']
            res.append(result)
        output['total_cost'] = total_cost
        output['spots'] = res
        return Response(self.get_data(output), status=status.HTTP_200_OK)

class CancelReservations(AppResponse, GenericAPIView):
    """
    Cancel reservation API for user
    """
    serializer_class = None

    @swagger_auto_schema(
        manual_parameters=[auth, reserve_id],
        responses={
            200: GenericRespSerializer,
            400: GenericRespSerializer,
        }
    )
    def delete(self, request, format=None):
        output = dict()

        try:
            resv_id = request.GET['reserve_id']
        except Exception as e:
            output['message'] = 'NO_RESERVE_ID'
            return Response(self.get_data(output), status=status.HTTP_400_BAD_REQUEST)
        resv_obj = Reservations.objects.select_related('spot').filter(pk=resv_id).first()
        if not resv_obj:
            output['message'] = 'WRONG_RESERVE_ID'
            return Response(self.get_data(output), status=status.HTTP_400_BAD_REQUEST)

        spot_obj = resv_obj.spot
        spot_obj.is_reserved = False
        spot_obj.save()
        cost, _ = calculate_reservation_spot_cost(resv_obj)
        resv_obj.delete()
        output['message'] = 'CANCEL_SUCCESS'
        output['cost'] = cost
        return Response(self.get_data(output), status=status.HTTP_200_OK)