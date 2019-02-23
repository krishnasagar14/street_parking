from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import exceptions, status
from drf_yasg.utils import swagger_auto_schema

from core.views import AppResponse
from core import JWT_tokenizer, KEY_AUDIENCE
from common.serializers import GenericRespSerializer
from common.helpers import check_user_staff_superuser, is_user_active
from .serializers import LoginReqSerializer, LoginRespSerializer
# Create your views here.

class Login(AppResponse, GenericAPIView):
    """
    Login View serving /login endpoint for portal's users.
    """
    authentication_classes = ()
    serializer_class = LoginReqSerializer

    @swagger_auto_schema(
        responses={
            200: LoginRespSerializer,
            400: GenericRespSerializer,
        }
    )
    def post(self, request, format=None):
        output = dict()
        email = request.data.get('email')
        passw = request.data.get('password')

        def _resp_400():
            return Response(self.get_data(output), status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=passw)
        token = None
        if user:
            if check_user_staff_superuser(user):
                output['message'] = 'USER_IS_ADMIN'
                return _resp_400()
            if not is_user_active(user):
                output['message'] = 'USER_NOT_FOUND'
                return _resp_400()  
            payload = {
                KEY_AUDIENCE: user.id.hex
            }
            token = JWT_tokenizer.tokenize(payload)
            output['token'] = token
            return Response(self.get_data(output), status=status.HTTP_200_OK)
        else:
            output['message'] = 'INVALID_CREDENTIALS'
            return _resp_400()