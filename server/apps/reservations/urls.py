from django.urls import path

from .views import StreetSpotReservation

app_name = 'reservations'

urlpatterns = [
    path('spot/', StreetSpotReservation.as_view()),
]