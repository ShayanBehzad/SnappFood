from re import A
from django.contrib import admin
from .models import * 
from dashboard.models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from register.forms import Registerform
from .forms import * 

# Register your models here.


# Use if you want to use admin-panel for user registration:
# class SellerInline(admin.StackedInline):
#     model = Seller
#     can_delete = False
#     verbose_name_plural = "seller"

# class UserAdmin(BaseUserAdmin):

#     inlines = [SellerInline]






@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'restaurant_type', 'phone']
    filter_horizontal = ('foods',)
    raw_id_fields = ['seller']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['cus', 'restaurant', 'content','amount_paid', 'state']
    # filter_horizontal = ('content',)

    def customer(self, obj):
        return obj

    # def get_cphone(self, obj):
    #     return obj.phone
    
    # def get_subscription(self, obj):
    #     return obj.subscription
    
    # get_subscription.short_description = 'subscription'
    # get_cphone.short_description = 'phone'


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'category', 'price', 'discount', 'selling_price']

# class UserAdmin(admin.ModelAdmin):
#     list_display = ['id' ,'username', 'email', 'is_staff']




# class ScheduleInline(admin.TabularInline):
#     model = WorkingHour

# class HoursAdmin(admin.ModelAdmin):
#     inlines = [
#         ScheduleInline,
#     ]



admin.site.register(RestaurantAddress)
admin.site.register(State)
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
admin.site.unregister(Food)
admin.site.register(Food, FoodAdmin)
admin.site.unregister(Restaurant)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(RestCategory)
admin.site.register(FoodCategory)
admin.site.unregister(Order)
admin.site.register(Order, OrderAdmin)
# admin.site.register(Schedule, HoursAdmin)
admin.site.register(Schedule)
admin.site.register(WorkingHour)