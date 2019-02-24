from django.test import TestCase
from rest_framework.test import APIRequestFactory

from .views import ParkingSpotsAvail, SearchParkingSpot
from .models import parkingSpot
from common.tests import prepare_dummy_user_data, USER_DATA
from core import JWT_tokenizer, KEY_AUDIENCE
from apps.user.models import User

# Create your tests here.

class ApiTests(TestCase):
    factory = APIRequestFactory()

    def setUp(self):
        prepare_dummy_user_data()

    def test_available_spots(self):
        view = ParkingSpotsAvail.as_view()
        req = self.factory.get('/spots/available/')
        resp = view(req)
        st_code = resp.status_code
        rdata = resp.data.get('data')
        self.assertEqual(st_code, 200)
        self.assertGreaterEqual(len(rdata), 1)
        print("Available spots API test success")

    def test_search_spots(self):
        user_obj = User.objects.filter(email=USER_DATA['email']).first()
        view = SearchParkingSpot.as_view()
        req = self.factory.get('/spots/search/')
        resp = view(req)
        st_code = resp.status_code
        self.assertEqual(st_code, 401)

        url = '/spots/search/?radius={}&Latitude={}&Longitude={}'.format(20, 1, 36)
        payload = {
            KEY_AUDIENCE: user_obj.id.hex
        }
        token = JWT_tokenizer.tokenize(payload)
        req = self.factory.get(url, HTTP_AUTHORIZATION='Bearer '+ token)
        resp = view(req)
        st_code = resp.status_code
        rdata = resp.data.get('data')
        self.assertEqual(st_code, 200)
        self.assertGreaterEqual(len(rdata), 0)
        print("Search spot API test success")