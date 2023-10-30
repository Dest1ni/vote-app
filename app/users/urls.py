from django.urls import path
from .views import *


app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name = "users-login"),
    path('logout/', LogoutView.as_view(), name = "users-logout"),
    path('registration/', RegistrationView.as_view(), name = "users-registration"),
]
