from django.urls import path

from .views import ParkingSpotsAvail, SearchParkingSpot

app_name = 'parkSpot'

urlpatterns = [
    path('spots/available/', ParkingSpotsAvail.as_view()),
    path('spots/search/', SearchParkingSpot.as_view()),
]