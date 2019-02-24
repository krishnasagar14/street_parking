from drf_yasg import openapi

reserve_id = openapi.Parameter(
    'reserve_id',
    in_=openapi.IN_QUERY,
    required=True,
    description='Reservation id for cancel action',
    type=openapi.TYPE_STRING,
)