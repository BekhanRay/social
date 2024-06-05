from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Profile


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Login'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

    # class Meta:
    #     model = User
    #     fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        error_messages={'required': 'Email is required'}
    )
    birthdate = forms.DateField(
        error_messages={'required': 'We need to know your age !'}
    )

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


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'