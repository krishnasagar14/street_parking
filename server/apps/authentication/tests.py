from django.test import TestCase
from rest_framework.test import APIRequestFactory

from .views import LoginView, SignupView
from common.tests import USER_DATA, prepare_dummy_user_data

# Create your tests here.

class ApiViewTests(TestCase):
    factory = APIRequestFactory()

    def test_signup(self):
        user_data = USER_DATA
        view = SignupView.as_view()

        req = self.factory.post('/register/', user_data, format='json')
        resp = view(req)
        st_code = resp.status_code
        self.assertEqual(st_code, 400)

        user_data['password'] = 'test01'
        req = self.factory.post('/register/', user_data, format='json')
        resp = view(req)
        st_code = resp.status_code
        rdata = resp.data.get('data')
        self.assertEqual(st_code, 201)
        self.assertEqual(rdata['message'], 'USER_REGISTER_SUCCESS')
        print("User register API test success")

    def test_login(self):
        prepare_dummy_user_data()
        view = LoginView.as_view()

        user_data = {}

        req = self.factory.post('/login/', user_data, format='json')
        resp = view(req)
        st_code = resp.status_code
        self.assertEqual(st_code, 400)

        user_data = {
            'email': USER_DATA['email'],
            'password': '',
        }
        req = self.factory.post('/login/', user_data, format='json')
        resp = view(req)
        st_code = resp.status_code
        self.assertEqual(st_code, 400)

        user_data['password'] = 'test123'
        req = self.factory.post('/login/', user_data, format='json')
        resp = view(req)
        st_code = resp.status_code
        rdata = resp.data.get('data')
        self.assertEqual(st_code, 200)
        self.assertEqual(len(rdata['token'].split('.')), 3)
        print("User login API test success")