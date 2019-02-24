from django.urls import path

from .views import StreetSpotReservation, ViewReservations, CancelReservations

app_name = 'reservations'

urlpatterns = [
    path('spot/', StreetSpotReservation.as_view()),
    path('view/', ViewReservations.as_view()),
    path('cancel/', CancelReservations.as_view()),
]