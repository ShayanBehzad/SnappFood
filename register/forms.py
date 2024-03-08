from dataclasses import fields
from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, ModelForm
from django.core.validators import RegexValidator
from dashboard.models import *
from register.models import User


class Registerform(UserCreationForm):

#     phone_regex = RegexValidator(
#        regex=r'(0|\+98)?([ ]|-|[()]){0,2}9[1|2|3|4]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}',
#        message="Phone number must be entered in the format: '+989031234567'. Up to 15 digits allowed."
#    )
#     phone = forms.CharField(validators=[phone_regex], max_length=15)
#     # phone = forms.CharField(max_length=15)
    # role = forms.CharField(initial=User.SELLER, widget=forms.HiddenInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']



class RestAddressRegisterForm(ModelForm):
    class Meta:
        model = RestaurantAddress
        fields = ['city', 'address', 'latitude', 'longitude']



class RestRegisterForm(ModelForm):
    address = RestAddressRegisterForm
    class Meta:
        model = Restaurant
        fields = ['name', 'restaurant_type', 'phone', 'card_id']
