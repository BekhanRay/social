from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Login'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'login',
            'email',
            'nickname',
            'birthdate',
            'gender',
            'country',
            'region',
            'city',
            'user_agreement',
            'confirmation_code'
        ]
