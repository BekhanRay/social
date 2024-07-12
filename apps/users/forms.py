from django import forms
from django.contrib.auth.forms import PasswordChangeForm



class UserFilterForm(forms.Form):
    min_age = forms.IntegerField(required=False, label='Min Age')
    max_age = forms.IntegerField(required=False, label='Max Age')
    region = forms.CharField(max_length=50, required=False)
    city = forms.CharField(max_length=50, required=False)
    country = forms.CharField(max_length=255, required=False)
    gender = forms.CharField(required=False)
    is_online = forms.BooleanField(required=False)


class UserChangeForm(forms.Form):
    nickname = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(max_length=100, required=False)
    gender = forms.CharField(max_length=7, required=False)
    preffered_gender = forms.CharField(max_length=7, required=False)
    age = forms.IntegerField(required=False)
    region = forms.CharField(max_length=50, required=False)
    city = forms.CharField(max_length=50, required=False)
    country = forms.CharField(max_length=50, required=False)
    general_info = forms.CharField(widget=forms.Textarea, required=False)
    personal_info = forms.CharField(widget=forms.Textarea, required=True)
    education_profession = forms.CharField(widget=forms.Textarea, required=False)
    habits_preferences = forms.CharField(widget=forms.Textarea, required=False)


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(attrs={'class': 'input_design'}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'input_design'}))
    new_password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'class': 'input_design'}))