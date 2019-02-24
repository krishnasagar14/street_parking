import time

from django.test import TestCase
from rest_framework import exceptions

from .views import AppResponse
from .exceptionsHandlers import ApplnExceptionHandler
from .authMech.jwt import JWT

# Create your tests here.

class AppResponseTest(TestCase):

    def test_struct(self):
        data = {'a': 1}
        out = AppResponse().get_data(data)
        self.assertEqual(out['data'], data)
        print("AppResponse test success")

class CustomExceptionHandlerTest(TestCase):

    def test_exception(self):
        resp = ApplnExceptionHandler(exceptions.APIException(), {})
        self.assertEqual(resp.status_code, 500)
        print("Custom Exception handler test success")

class JwtTest(TestCase):
    jwt_tokenizer = JWT('dfd98724548asbd#%%^*&!@#$', token_expiry=2)

    def test_tokenize(self):
        data = {'key': '23492woih9890324876712e<<myJWT>>'}
        tk = self.jwt_tokenizer.tokenize(data)
        self.assertEqual(len(tk.split('.')), 3)

        tampered_tk = tk[:16]
        try:
            r_data = self.jwt_tokenizer.detokenize(tampered_tk)
        except Exception as e:
            self.assertEqual('not enough values to unpack (expected 3, got 1)', str(e))

        time.sleep(1)
        r_data = self.jwt_tokenizer.detokenize(tk)
        self.assertEqual(r_data, data)

        time.sleep(4)
        try:
            r_data = self.jwt_tokenizer.detokenize(tk)
        except Exception as e:
            self.assertEqual(str(e), 'Received token is expired.')
        print("JWT tokenize test success")