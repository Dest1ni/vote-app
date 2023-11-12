from django.shortcuts import render
from django.contrib.auth.views import LoginView as BaseLoginView,LogoutView as BaseLogoutView
from django.views.generic import CreateView
from .models import UserModel
from .forms import RegistrationForm

class LoginView(BaseLoginView):
    template_name = 'users/auth/login.html'

class LogoutView(BaseLogoutView):
    pass

class RegistrationView(CreateView):
    model = UserModel
    form_class = RegistrationForm
    template_name = "users/auth/registration.html"
    