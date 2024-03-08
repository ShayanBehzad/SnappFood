from django.conf import settings
from django.db import models
from django.urls import reverse
# from django.contrib.auth.models import User,AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MinValueValidator, RegexValidator
from register.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import date
from dashboard.models import *
from django.db.models import Q
import random
import uuid
todey = date.today()
    



class Customer(models.Model):
    # subscription = models.UUIDField( 
    #      primary_key = True, 
    #      default = uuid.uuid4, 
    #      editable = False)
    subscription = models.AutoField(primary_key=True, unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    # email = models.EmailField()
    class Meta:
        db_table = 'custapi_customer'

    def __str__(self):
        return f'{self.user}'



class Address(models.Model):
    title = models.CharField(max_length=20)

    address = models.TextField()

    # cities = models.TextChoices('cities', 'Rasht Lahijan Tehran Karaj Ghazvin Tabriz Booshehr Bandar_abbas Mashhad')

    city = models.CharField(max_length=30, choices=RestaurantAddress.cities.choices)


    latitude = models.CharField(max_length=30)

    longitude = models.CharField(max_length=30)

    cust = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



class Cart(models.Model):
    # id
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='restaurant')
    # change it to Customer
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.id} , {self.customer}'



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='foods')
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='cart_foods')
    count = models.IntegerField()
    
    @property
    def price(self):
        return self.food.selling_price * self.count
    
    def save(self, *args, **kwargs):
        foods = CartItem.objects.filter(Q(food=self.food) , Q(cart=self.cart))
        # kir = CartItem.objects.get(Q(food=self.food) , Q(cart=self.cart))

        for food in foods:
            print(self.food.id)
            print(food.food.id)
            if self.food.id == food.food.id:
                count = self.count + food.count
                CartItem.objects.filter(cart=self.cart, food=self.food).update(count=count)
                # CartItem.objects.create(cart=self.cart, food=self.food, count=count)
                print('ananas')
                return None
            print('golabi')
        print('neh')
        super().save(*args, **kwargs)

    

    def __str__(self):
        return f"{self.food} - Count: {self.count}"




SCORE_CHOICES = (
    ('1', '*'),
    ('2', '**'),
    ('3', '***'),
    ('4', '****'),
    ('5', '*****')
)

class Comment(models.Model):
    # change it to Customer
    author = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='author')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='comment_restaurant')
    # the author's order(not corrected)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    score = models.CharField(max_length=6, choices=SCORE_CHOICES, default='')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.restaurant.rating = self.restaurant.average_score
        self.restaurant.save()

    def __str__(self):
        return self.content


class AnswerComment(models.Model):
    answer = models.TextField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='answer')

    def __str__(self):
        return f'{self.comment}'
