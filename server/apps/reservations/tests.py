from django.test import TestCase
from rest_framework.test import APIRequestFactory

from common.tests import prepare_dummy_user_data, USER_DATA
from core import JWT_tokenizer, KEY_AUDIENCE
from .models import Reservations
from apps.parkSpot.models import parkingSpot
from apps.user.models import User
from .views import StreetSpotReservation, ViewReservations, CancelReservations

# Create your tests here.

class ModelTest(TestCase):

    def setUp(self):
        prepare_dummy_user_data()
        spot_obj = parkingSpot.objects.first()
        user_obj = User.objects.filter(email=USER_DATA['email']).first()
        reserv_data = {
            'duration': 1,
            'user': user_obj,
            'spot': spot_obj,
        }
        Reservations.objects.create(**reserv_data)

    def test_model(self):
        resv_obj = Reservations.objects.first()
        self.assertEqual(resv_obj.duration, 1)
        print("Reservations model test success")

class ApiTests(TestCase):
    factory = APIRequestFactory()

    def setUp(self):
        prepare_dummy_user_data()
        self.user_obj = User.objects.first()
        payload = {
            KEY_AUDIENCE: self.user_obj.id.hex
        }
        self.token = JWT_tokenizer.tokenize(payload)
        self.spot_obj = parkingSpot.objects.first()

    def test_reserve_spot(self):
        view = StreetSpotReservation.as_view()
        data = {
            'spot_id': self.spot_obj.id.hex
        }
        data['duration'] = 1
        req = self.factory.post('/spot/', data, HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = view(req)
        st_code = resp.status_code
        self.assertEqual(st_code, 200)
        rdata = resp.data.get('data')
        self.assertEqual(rdata['message'], 'SPOT_RESERVED')

        print("Reserve spot API test success")

    def test_reserve_spot_negative(self):
        view = StreetSpotReservation.as_view()
        data = {}
        req = self.factory.post('/spot/', data, HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = view(req)
        st_code = resp.status_code
        self.assertEqual(st_code, 400)

        data = {
            'spot_id': self.spot_obj.id.hex
        }
        req = self.factory.post('/spot/', data, HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = view(req)
        st_code = resp.status_code
        self.assertEqual(st_code, 400)
        print("Reserve spot API negative test success")

    def test_reserve_spot_already_reserved(self):
        view = StreetSpotReservation.as_view()
        data = {
            'spot_id': self.spot_obj.id.hex
        }
        data['duration'] = 1
        req = self.factory.post('/spot/', data, HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = view(req)
        st_code = resp.status_code
        self.assertEqual(st_code, 400)
        print("Reserve slready reserved pot API test success")


    def test_view_reservations(self):
        view = ViewReservations.as_view()
        req = self.factory.get('/view/', HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = view(req)
        st_code = resp.status_code
        self.assertEqual(st_code, 200)
        print("View reservations API test success")

    def _create_dummy_resv_data(self):
        reserv_data = {
            'duration': 1,
            'user': self.user_obj,
            'spot': self.spot_obj,
        }
        resv_obj = Reservations.objects.create(**reserv_data)

    def test_cancel_reservation(self):
        view = CancelReservations.as_view()
        self._create_dummy_resv_data()
        req = self.factory.delete('/cancel/?reserve_id={}'.format(resv_obj.id.hex), HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = view(req)
        st_code = resp.status_code
        self.assertEqual(st_code, 200)

        print("Cancel reservations API test success")

    def test_cancel_reservation_negative(self):
        self._create_dummy_resv_data()
        req = self.factory.delete('/cancel/', HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = view(req)
        st_code = resp.status_code
        self.assertEqual(st_code, 400)

        r_id = 'a2a35b1844cd45809667a3d84bff5ca1'
        req = self.factory.delete('/cancel/?reserve_id={}'.format(r_id),
                                  HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = view(req)
        st_code = resp.status_code
        self.assertEqual(st_code, 400)

        print("Cancel reservations API negative test success")
