from drf_yasg import openapi

radius = openapi.Parameter(
    'radius',
    in_= openapi.IN_QUERY,
    type=openapi.TYPE_NUMBER,
    description='radius in meters',
    required=True,
)

lat = openapi.Parameter(
    'Latitude',
    in_=openapi.IN_QUERY,
    type=openapi.TYPE_INTEGER,
    description='latitude of location',
    required=True,
)

longi = openapi.Parameter(
    'Longitude',
    in_=openapi.IN_QUERY,
    type=openapi.TYPE_INTEGER,
    description='longitude of location',
    required=True,
)