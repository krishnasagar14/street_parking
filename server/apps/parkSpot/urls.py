from django.urls import path

from .views import ParkingSpotsAvail

app_name = 'parkSpot'

urlpatterns = [
    path('spots/available/', ParkingSpotsAvail.as_view()),
]