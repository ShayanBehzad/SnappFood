from django.urls import path
from . import views


urlpatterns = [
    path('register/restaurant_form/', views.restregister, name='restaurantpage'),
    path('reister/restaurant_form/address/', views.restaddressregister, name='restaddress'),
    path('register/', views.register, name='registerpage'),
    path('test/', views.test, name='test'),

]
