from django import forms
from .models import UserModel
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['username','password1','password2']
