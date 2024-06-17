from django import forms


class UserFilterForm(forms.Form):
    min_age = forms.IntegerField(required=False, label='Min Age')
    max_age = forms.IntegerField(required=False, label='Max Age')
    region = forms.CharField(max_length=50, required=False)
    city = forms.CharField(max_length=50, required=False)
    country = forms.CharField(max_length=255, required=False)
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')], required=False)
    is_online = forms.BooleanField(required=False)
