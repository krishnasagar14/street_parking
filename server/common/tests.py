from django.test import TestCase

from .models import baseModel
from .helpers import *
from apps.user.models import User
# Create your tests here.

def prepare_dummy_user_data():
    user_data = {
        'email': 'test_user1@mailinator.com',
        'first_name': 'test_user1',
        'last_name': 'user1',
        'mobile_no': '1111111',
    }
    user_obj = User.objects.create(**user_data)
    user_obj.set_password('test123')
    user_obj.save()


class BaseModelTest(TestCase):

    def setUp(self):
        baseModel.objects.create()

    def test_model(self):
        base_obj = baseModel.objects.first()
        self.assertNotEqual(base_obj, None)
        self.assertEqual(base_obj.created_by, 'app')
        print("Base model test success")

class HelperMethodsTest(TestCase):

    def setUp(self):
        prepare_dummy_user_data()

    def test_helpers(self):
        user_obj = User.objects.first()
        res = check_user_staff_superuser(user_obj)
        self.assertEqual(res, False)

        user_obj.is_staff = True
        user_obj.is_superuser = True
        res = check_user_staff_superuser(user_obj)
        self.assertEqual(res, True)

        res = is_user_active(user_obj)
        self.assertEqual(res, True)
        user_obj.is_active = False
        res = is_user_active(user_obj)
        self.assertEqual(res, False)
        print("Helper methods test success")