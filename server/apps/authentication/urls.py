from django.urls import path

from .views import LoginView, SignupView

app_name = 'authentication'

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', SignupView.as_view()),
]