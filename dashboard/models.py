from random import choices
from typing import Iterable
from django.db import models
from email.policy import default
from django.conf import settings
from django.db import models
from django.urls import reverse
# from django.contrib.auth.models import User,AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MinValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from register.models import User
from django.contrib.auth import get_user_model
from datetime import date



todey = date.today()





class RestCategory(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ["-name"]
    def __str__(self):
        return self.name


class FoodCategory(models.Model):
    FoodCategory = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Food Category'
        verbose_name_plural = 'Food Categories'

    def __str__(self):
        return self.FoodCategory


class Food(models.Model):
    name = models.CharField(max_length=20)
    ingredients = models.TextField(null=True)
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, related_name='category_foods')
    image = models.ImageField(upload_to='image/', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    is_available = models.BooleanField(default=True)
    discount = models.IntegerField(validators=[MinValueValidator(0)], default=0, null=True)
    selling_price = models.IntegerField(null=False)
    foodparty = models.BooleanField(default=False, null=True)

    @property
    def selling_price(self):
        return self.price - (self.discount * self.price ) / 100
    
    def get_absolute_url(self):
        from dashboard import views
        return reverse(views.editfoodform, kwargs={"food_id": self.id})
    
    def __str__(self):
        return self.name

    # https://docs.djangoproject.com/en/4.2/ref/models/options/
    # class Meta:
    #     order_with_respect_to = "category"


class WorkingHour(models.Model):
    start = models.TimeField()
    end = models.TimeField()
    days = models.TextChoices('days', 'saturday sunday monday thusday wednesday thursday friday')
    day = models.CharField( max_length=30, choices=days.choices)


    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.day

class Restaurant(models.Model):
    name = models.CharField(max_length=30)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='restaurant_owner')
    foods = models.ManyToManyField(Food, related_name='food')
    image = models.ImageField(upload_to='image/restaurant', null=True) 
    restaurant_type = models.ForeignKey(RestCategory, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=15)
    rating = models.FloatField(null=True, editable=False)
    card_id = models.BigIntegerField()
    shipping_cost = models.IntegerField(null=True)
    is_open = models.BooleanField(default=True)


    @property
    def comments_count(self):
        from custapi.models import Comment
        comments = Comment.objects.filter(restaurant=self)
        count = 0
        for i in comments:
            count += 1
        return count


    
    @property
    def average_score(self):
        from custapi.models import Comment
        comments = Comment.objects.filter(restaurant=self)
        rating = 0
        counter = 0
        avg = 0
        if comments.exists():
            for i in comments:
                rating += int(i.score)
                counter += 1
            avg = rating / counter
        return avg
    

    def __str__(self):
        return self.name

class Schedule(models.Model):

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='schedule')

    saturday = models.ForeignKey(WorkingHour, on_delete=models.CASCADE, related_name='saturday', null=True, blank=True)
    sunday = models.ForeignKey(WorkingHour, on_delete=models.CASCADE, related_name='sunday', null=True, blank=True)
    monday = models.ForeignKey(WorkingHour, on_delete=models.CASCADE, related_name='monday', null=True, blank=True)
    thusday = models.ForeignKey(WorkingHour, on_delete=models.CASCADE, related_name='thusday', null=True, blank=True)
    wednesday = models.ForeignKey(WorkingHour, on_delete=models.CASCADE, related_name='wednesday', null=True, blank=True)
    thursday = models.ForeignKey(WorkingHour, on_delete=models.CASCADE, related_name='thursday', null=True, blank=True)
    friday = models.ForeignKey(WorkingHour, on_delete=models.CASCADE, related_name='friday', null=True, blank=True)

    def __str__(self):
        return f'{self.restaurant}'
    
    
class RestaurantAddress(models.Model):
    cities = models.TextChoices('cities', 'Rasht Lahijan Tehran Karaj Ghazvin Tabriz Booshehr Bandar_abbas Mashhad')

    city = models.CharField(max_length=30, choices=cities.choices)

    address = models.TextField()

    latitude = models.CharField(max_length=30)

    longitude = models.CharField(max_length=30)

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='address')

    def __str__(self):
        return self.city



class State(models.Model):
    is_pending = models.BooleanField(default=True)
    is_preparing = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    st = models.CharField(max_length=10)

    @property
    def st(self):
        if self.is_delivered:
            return 'delivered'
        elif self.is_sent:
            return 'sent'
        elif self.is_preparing:
            return 'preparing'
        else:
            return 'pending'
    def __str__(self):
        return self.st




class Order(models.Model):
    customer = models.ForeignKey('custapi.Customer', on_delete=models.CASCADE, name='cus', default=None)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    state = models.ForeignKey(State, default="is_pending", on_delete=models.CASCADE)
    content = models.JSONField()
    amount_paid = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'{self.id}'
    





