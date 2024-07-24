from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import User

# # Check if User model is registered before unregistering
# if admin.site.is_registered(User):
#     admin.site.unregister(User)

# # Register your custom User model
# admin.site.register(User, UserAdmin)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'role']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)