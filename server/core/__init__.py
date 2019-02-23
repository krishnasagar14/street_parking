from django.conf import settings

from .authMech.jwt import JWT, KEY_AUDIENCE

BEARER_TOKEN_EXPIRY = 12 * 60 * 60
JWT_tokenizer = JWT(settings.SECRET_KEY, token_expiry=BEARER_TOKEN_EXPIRY)