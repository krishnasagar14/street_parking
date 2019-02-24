from rest_framework.authentication import BaseAuthentication
from rest_framework import HTTP_HEADER_ENCODING, exceptions, status
from django.utils.six import text_type

from apps.user.models import User
from core import JWT_tokenizer, KEY_AUDIENCE

def get_auth_header_value(request):
    """
    Returns HTTP_AUTHORIZATION header value from request object
    :param request: request object
    :return: header value string
    """
    auth_value = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth_value, text_type):
        # workaround for django test client unicode scheme
        auth_value = auth_value.encode(HTTP_HEADER_ENCODING)
    return auth_value


class BearerAuthentication(BaseAuthentication):
    """
    This custom authentication mechanism is for bearer based auth captured from
    HTTP_AUTHORIZATION http header key.
    DRF BaseAuthentication class extended and such class is appended into DRF settings.
    Reference: https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication
    eg:
    'Bearer eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJrZXkiOiAiMjM0OTJ3b2loOTg5MDMy\
    NDg3NjcxMmY8PG15SldUPj4iLCAiaWF0IjogMTU1MDkzNTI3OTY5MH0=.ac9ad606be67fa3d98f5f5dd8\
    d2d1a0675329527a516cace73fa6c7829290444'
    The clients need to pass such request header which will be checked by such mechanism.
    """

    keyword = 'Bearer'
    model = User
    jwt = JWT_tokenizer

    def get_model(self):
        return self.model

    def authenticate_token(self, token, request):
        model = self.get_model()
        token_data = None
        user = None
        try:
            token_data = self.jwt.detokenize(token)
        except Exception as e:
            raise exceptions.AuthenticationFailed('INVALID_TOKEN')
        if not token_data:
            raise exceptions.AuthenticationFailed('NO_TOKEN_FOUND')

        try:
            user_id = token_data.get(KEY_AUDIENCE, '')
            user = User.objects.filter(pk=user_id).first()
        except Exception as e:
            raise exceptions.AuthenticationFailed('INCORRECT_TOKEN_DATA')
        if not user:
            raise exceptions.AuthenticationFailed('NO_USER_FOUND')
        return (user, token_data)

    def authenticate(self, request):
        auth = get_auth_header_value(request)
        auth = auth.split()

        try:
            if auth[0].title() != self.keyword:
                raise exceptions.AuthenticationFailed('NO_BEARER_FOUND')
        except Exception as e:
                raise exceptions.AuthenticationFailed('INVALID_AUTH_MECHANISM')

        token = None
        try:
            token = auth[1].decode('utf-8')
        except UnicodeError as e:
            errmsg = 'INVALID_TOKEN_DATA'
            raise exceptions.AuthenticationFailed(errmsg)

        return self.authenticate_token(token, request)

    def authenticate_header(self, request):
        return self.keyword
