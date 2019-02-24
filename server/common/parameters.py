from drf_yasg import openapi

# Authorization request header defination for APIs
auth = openapi.Parameter(
    'Authorization',
    in_=openapi.IN_HEADER,
    type=openapi.TYPE_STRING,
    required=True,
    description='Bearer authorization token'
)