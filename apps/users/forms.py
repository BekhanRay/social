from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, Profile


class UserRegistrationForm(UserCreationForm):

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True, label='Birthdate')
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
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

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Login'})
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
        self.fields['nickname'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nickname'})
        self.fields['country'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'})
        self.fields['region'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Region'})
        self.fields['city'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'})
        self.fields['user_agreement'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
        self.fields['confirmation_code'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Confirmation Code'})


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = {
            'general_info',
            'personal_info',
            'education_profession',
            'habits_preferences',
        }
        widgets = {
            'user': forms.HiddenInput(),
        }