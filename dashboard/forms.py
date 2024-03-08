from ast import Mod
from dataclasses import field
from email.mime import image
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, ModelForm
from django.core.validators import RegexValidator
from register.models import User
from .models import *



class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = ['image', 'name', 'ingredients', 'category', 'price', 'discount','is_available', 'foodparty']

class StateForm(forms.Form):
    choises = (('1', 'pending'), ('2', 'preparing'), ('3', 'sent'), ('4', 'delivered'))
    fields = forms.ChoiceField(widget=forms.Select,choices=choises)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

class OrderState(ModelForm):
    class Meta:
        model = Order
        fields = ['state']

class RestAddressRegisterForm(ModelForm):
    class Meta:
        model = RestaurantAddress
        fields = ['city', 'address', 'latitude', 'longitude']


class RestScheduleRegisterForm(ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'


class RestSettings(ModelForm):
    class Meta:
        model = Restaurant
        fields = ['image', 'name', 'restaurant_type', 'phone', 'is_open', 'shipping_cost']

class WorkingHourForm(ModelForm):
    class Meta:
        model = WorkingHour
        fields = '__all__'
